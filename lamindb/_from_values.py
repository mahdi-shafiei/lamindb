from typing import Any, Dict, Iterable, List, Tuple, Union

import pandas as pd
from django.core.exceptions import FieldDoesNotExist
from django.db.models.query_utils import DeferredAttribute as Field
from lamin_logger import colors, logger
from lnschema_core.models import ORM
from lnschema_core.types import ListLike

from ._select import select
from .dev._settings import settings


# The base function for `from_values`
def get_or_create_records(
    iterable: ListLike,
    field: Field,
    *,
    from_bionty: bool = False,
    **kwargs,
) -> List:
    """Get or create records from iterables."""
    upon_create_search_names = settings.upon_create_search_names
    settings.upon_create_search_names = False
    try:
        field_name = field.field.name
        model = field.field.model
        iterable_idx = index_iterable(iterable)

        records, nonexist_values = get_existing_records(
            iterable_idx=iterable_idx, field=field, kwargs=kwargs
        )

        # new records to be created based on new values
        if len(nonexist_values) > 0:
            if from_bionty:
                records_bionty, unmapped_values = create_records_from_bionty(
                    iterable_idx=nonexist_values, field=field, **kwargs
                )
                records += records_bionty
            else:
                unmapped_values = nonexist_values
            # unmapped new_ids will only create records with field and kwargs
            if len(unmapped_values) > 0:
                for i in unmapped_values:
                    records.append(model(**{field_name: i}, **kwargs))
                logger.info(
                    "Created"
                    f" {colors.red(f'{len(unmapped_values)} {model.__name__} records')}"
                    f" with a single field {colors.red(f'{field_name}')}"
                )
        return records
    finally:
        settings.upon_create_search_names = upon_create_search_names


def get_existing_records(iterable_idx: pd.Index, field: Field, kwargs: Dict = {}):
    field_name = field.field.name
    model = field.field.model
    condition: Dict = {}

    if _has_species_field(model):
        from lnschema_bionty._bionty import create_or_get_species_record

        species_record = create_or_get_species_record(
            species=kwargs.get("species"), orm=model
        )
        if species_record is not None:
            kwargs.update({"species": species_record})
            condition.update({"species__name": species_record.name})

    # map synonyms based on the DB reference
    syn_mapper = model.map_synonyms(
        iterable_idx, species=kwargs.get("species"), return_mapper=True
    )

    syn_msg = ""
    if len(syn_mapper) > 0:
        syn_msg = (
            "Returned"
            f" {colors.green(f'{len(syn_mapper)} existing {model.__name__} DB records')} that"  # noqa
            f" matched {colors.green('synonyms')}"
        )
        iterable_idx = iterable_idx.to_frame().rename(index=syn_mapper).index

    # get all existing records in the db
    # if necessary, create records for the values in kwargs
    # k:v -> k:v_record
    # kwargs is used to deal with species
    condition.update({f"{field_name}__in": iterable_idx.values})

    stmt = select(model, **condition)

    records = stmt.list()  # existing records
    n_name = len(records) - len(syn_mapper)
    if n_name > 0:
        logger.info(
            "Returned"
            f" {colors.green(f'{n_name} existing {model.__name__} DB records')} that"
            f" matched {colors.green(f'{field_name}')} field"
        )
    # make sure that synonyms logging appears after the field logging
    if len(syn_msg) > 0:
        logger.info(syn_msg)

    existing_values = iterable_idx.intersection(stmt.values_list(field_name, flat=True))
    nonexist_values = iterable_idx.difference(existing_values)

    return records, nonexist_values


def create_records_from_bionty(
    iterable_idx: pd.Index,
    field: Field,
    **kwargs,
):
    model = field.field.model
    field_name = field.field.name
    records: List = []
    # populate additional fields from bionty
    from lnschema_bionty._bionty import get_bionty_source_record

    # create the corresponding bionty object from model
    bionty_object = model.bionty(species=kwargs.get("species"))
    # add bionty_source record to the kwargs
    kwargs.update({"bionty_source": get_bionty_source_record(bionty_object)})

    # filter the columns in bionty df based on fields
    bionty_df = _filter_bionty_df_columns(model=model, bionty_object=bionty_object)

    # map synonyms in the bionty reference
    try:
        syn_mapper = bionty_object.map_synonyms(iterable_idx, return_mapper=True)
    except KeyError:
        # no synonyms column
        syn_mapper = {}
    msg_syn: str = ""
    if len(syn_mapper) > 0:
        msg_syn = (
            "Created"
            f" {colors.purple(f'{len(syn_mapper)} {model.__name__} records from Bionty')} that"  # noqa
            f" matched {colors.purple('synonyms')}"
        )
        iterable_idx = iterable_idx.to_frame().rename(index=syn_mapper).index

    # create records for values that are found in the bionty reference
    mapped_values = iterable_idx.intersection(bionty_df[field_name])

    if len(mapped_values) > 0:
        bionty_kwargs, multi_msg = _bulk_create_dicts_from_df(
            keys=mapped_values, column_name=field_name, df=bionty_df
        )
        for bk in bionty_kwargs:
            records.append(model(**bk, **kwargs))

        # logging of BiontySource linking
        source_msg = (
            ""
            if kwargs.get("bionty_source") is None
            else f", linked to BiontySource id={kwargs.get('bionty_source').id}"  # type:ignore # noqa
        )

        # number of records that matches field (not synonyms)
        n_name = len(records) - len(syn_mapper)
        if n_name > 0:
            msg = (
                "Created"
                f" {colors.purple(f'{n_name} {model.__name__} records from Bionty')} that"  # noqa
                f" matched {colors.purple(f'{field_name}')} field"
            )
            logger.info(msg + source_msg)
        # make sure that synonyms logging appears after the field logging
        if len(msg_syn) > 0:
            logger.info(msg_syn + source_msg)
        # warning about multi matches
        if len(multi_msg) > 0:
            logger.warning(multi_msg)

    # return the values that are not found in the bionty reference
    unmapped_values = iterable_idx.difference(mapped_values)
    return records, unmapped_values


def index_iterable(iterable: Iterable) -> pd.Index:
    idx = pd.Index(iterable).unique()
    # No entries are made for NAs, '', None
    # returns an ordered unique not null list
    return idx[(idx != "") & (~idx.isnull())]


def _filter_bionty_df_columns(model: ORM, bionty_object: Any) -> pd.DataFrame:
    bionty_df = pd.DataFrame()
    if bionty_object is not None:
        model_field_names = {i.name for i in model._meta.fields}
        # parents needs to be added here as relationships aren't in fields
        model_field_names.add("parents")
        bionty_df = bionty_object.df().reset_index()
        # rename definition to description for the lnschema_bionty
        bionty_df.rename(columns={"definition": "description"}, inplace=True)
        bionty_df = bionty_df.loc[:, bionty_df.columns.isin(model_field_names)]
    return bionty_df


def _bulk_create_dicts_from_df(
    keys: Union[set, List], column_name: str, df: pd.DataFrame
) -> Tuple[Dict, str]:
    """Get fields from a DataFrame for many rows."""
    multi_msg = ""
    if df.index.name != column_name:
        df = df.set_index(column_name).loc[list(keys)]
    if not df.index.is_unique:
        # return all records for multi-matches with a warning
        dup = df.index[df.index.duplicated()].unique().tolist()
        multi_msg = f"Multiple matches found in Bionty for: {dup}"

    return df.reset_index().to_dict(orient="records"), multi_msg


def _has_species_field(orm: ORM) -> bool:
    try:
        orm._meta.get_field("species")
        return True
    except FieldDoesNotExist:
        return False
