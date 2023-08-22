from typing import Dict, Iterable, List, Literal, Optional, Set, Union

import numpy as np
import pandas as pd
from django.core.exceptions import FieldDoesNotExist
from django.db.models import QuerySet
from lamin_utils import colors, logger
from lamin_utils._inspect import InspectResult
from lamindb_setup.dev._docs import doc_args
from lnschema_core import Registry, ValidationMixin
from lnschema_core.types import ListLike, StrField

from lamindb.dev.utils import attach_func_to_class_method

from . import _TESTING
from ._from_values import _has_species_field, _print_values
from ._registry import get_default_str_field


@classmethod  # type: ignore
@doc_args(ValidationMixin.inspect.__doc__)
def inspect(
    cls,
    values: ListLike,
    field: Optional[Union[str, StrField]] = None,
    *,
    mute: bool = False,
    **kwargs,
) -> InspectResult:
    """{}"""
    return _inspect(
        cls=cls,
        values=values,
        field=field,
        mute=mute,
        **kwargs,
    )


@classmethod  # type: ignore
@doc_args(ValidationMixin.validate.__doc__)
def validate(
    cls,
    values: ListLike,
    field: Optional[Union[str, StrField]] = None,
    *,
    mute: bool = False,
    **kwargs,
) -> np.ndarray:
    """{}"""
    return _validate(cls=cls, values=values, field=field, mute=mute, **kwargs)


def _inspect(
    cls,
    values: ListLike,
    field: Optional[Union[str, StrField]] = None,
    *,
    mute: bool = False,
    **kwargs,
) -> Union["pd.DataFrame", Dict[str, List[str]]]:
    """{}"""
    from lamin_utils._inspect import inspect

    if isinstance(values, str):
        values = [values]

    field = get_default_str_field(cls, field=field)

    orm = cls.model if isinstance(cls, QuerySet) else cls

    # inspect in the DB
    result_db = inspect(
        df=_filter_query_based_on_species(orm=orm, species=kwargs.get("species")),
        identifiers=values,
        field=str(field),
        mute=mute,
        **kwargs,
    )
    nonval = set(result_db.non_validated).difference(result_db.synonyms_mapper.keys())

    if len(nonval) > 0 and orm.__get_schema_name__() == "bionty":
        bionty_result = orm.bionty(species=kwargs.get("species")).inspect(
            values=nonval, field=str(field), mute=True, **kwargs
        )
        bionty_validated = bionty_result.validated
        bionty_mapper = bionty_result.synonyms_mapper
        hint = False
        if len(bionty_validated) > 0 and not mute:
            print_values = _print_values(bionty_validated)
            s = "" if len(bionty_validated) == 1 else "s"
            logger.info(
                f"-- detected {len(bionty_validated)} term{s} in Bionty for"
                f" {str(field)}: {print_values}"
            )
            hint = True

        if len(bionty_mapper) > 0 and not mute:
            print_values = _print_values(list(bionty_mapper.keys()))
            s = "" if len(bionty_mapper) == 1 else "s"
            logger.info(
                f"-- detected {len(bionty_mapper)} term{s} in Bionty as synonym{s}:"
                f" {print_values}"
            )
            hint = True

        if hint:
            logger.hint(
                "   add records from Bionty to your registry via"
                f" {colors.italic('.from_values()')}"
            )

    return result_db


def _validate(
    cls,
    values: ListLike,
    field: Optional[Union[str, StrField]] = None,
    *,
    mute: bool = False,
    **kwargs,
) -> np.ndarray:
    """{}"""
    from lamin_utils._inspect import validate

    return_str = True if isinstance(values, str) else False
    if isinstance(values, str):
        values = [values]

    field = get_default_str_field(cls, field=field)

    orm = cls.model if isinstance(cls, QuerySet) else cls
    field_values = pd.Series(
        _filter_query_based_on_species(
            orm=orm,
            species=kwargs.get("species"),
            values_list_field=field,
        ),
        dtype="object",
    )

    result = validate(
        identifiers=values,
        field_values=field_values,
        case_sensitive=True,
        mute=mute,
        field=field,
        **kwargs,
    )
    if return_str and len(result) == 1:
        return result[0]
    else:
        return result


@classmethod  # type: ignore
@doc_args(ValidationMixin.standardize.__doc__)
def standardize(
    cls,
    values: Iterable,
    field: Optional[Union[str, StrField]] = None,
    *,
    return_mapper: bool = False,
    case_sensitive: bool = False,
    mute: bool = False,
    bionty_aware: bool = True,
    keep: Literal["first", "last", False] = "first",
    synonyms_field: str = "synonyms",
    **kwargs,
) -> Union[List[str], Dict[str, str]]:
    """{}"""
    return _standardize(
        cls=cls,
        values=values,
        field=field,
        return_mapper=return_mapper,
        case_sensitive=case_sensitive,
        mute=mute,
        bionty_aware=bionty_aware,
        keep=keep,
        synonyms_field=synonyms_field,
        **kwargs,
    )


def set_abbr(self, value: str):
    if hasattr(self, "name") and value == self.name:
        pass
    else:
        try:
            self.add_synonym(value, save=False)
        except NotImplementedError:
            pass
    if not hasattr(self, "abbr"):
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute 'abbr'"
        )
    self.abbr = value
    if not self._state.adding:
        self.save()


def add_synonym(
    self,
    synonym: Union[str, ListLike],
    force: bool = False,
    save: Optional[bool] = None,
):
    _check_synonyms_field_exist(self)
    _add_or_remove_synonyms(
        synonym=synonym, record=self, force=force, action="add", save=save
    )


def remove_synonym(self, synonym: Union[str, ListLike]):
    _check_synonyms_field_exist(self)
    _add_or_remove_synonyms(synonym=synonym, record=self, action="remove")


def _standardize(
    cls,
    values: Iterable,
    field: Optional[Union[str, StrField]] = None,
    *,
    return_mapper: bool = False,
    case_sensitive: bool = False,
    mute: bool = False,
    bionty_aware: bool = True,
    keep: Literal["first", "last", False] = "first",
    synonyms_field: str = "synonyms",
    **kwargs,
) -> Union[List[str], Dict[str, str]]:
    """{}"""
    from lamin_utils._map_synonyms import map_synonyms

    return_str = True if isinstance(values, str) else False
    if isinstance(values, str):
        values = [values]

    field = get_default_str_field(cls, field=field)
    orm = cls.model if isinstance(cls, QuerySet) else cls

    species = kwargs.get("species")
    if _has_species_field(orm):
        # here, we can safely import lnschema_bionty
        from lnschema_bionty._bionty import create_or_get_species_record

        species_record = create_or_get_species_record(
            species=species,
            orm=orm.model if isinstance(orm, QuerySet) else orm,
        )
        species = species_record.name if species_record is not None else species_record

    try:
        orm._meta.get_field(synonyms_field)
        df = _filter_query_based_on_species(orm=orm, species=species)
    except FieldDoesNotExist:
        df = pd.DataFrame()

    _kwargs = dict(
        field=field,
        case_sensitive=case_sensitive,
        keep=keep,
        synonyms_field=synonyms_field,
    )
    # standardized names from the DB
    std_names_db = map_synonyms(
        df=df,
        identifiers=values,
        return_mapper=return_mapper,
        mute=mute,
        **_kwargs,
    )

    def _return(result: List, mapper: Dict, return_mapper: bool, return_str: bool):
        if return_mapper:
            return mapper
        else:
            if return_str and len(result) == 1:
                return result[0]
            return result

    # map synonyms in Bionty
    if orm.__get_schema_name__() == "bionty" and bionty_aware:
        mapper = {}
        if return_mapper:
            mapper = std_names_db
            std_names_db = map_synonyms(
                df=df, identifiers=values, return_mapper=False, mute=True, **_kwargs
            )

        val_res = orm.validate(std_names_db, field=field, mute=True, species=species)
        if all(val_res):
            return _return(
                result=std_names_db,
                mapper=mapper,
                return_mapper=return_mapper,
                return_str=return_str,
            )

        nonval = np.array(std_names_db)[~val_res]
        std_names_bt_mapper = orm.bionty(species=species).standardize(
            nonval, return_mapper=True, mute=True, **_kwargs
        )

        if len(std_names_bt_mapper) > 0 and not mute:
            s = "" if len(std_names_bt_mapper) == 1 else "s"
            warn_msg = (
                f"found {len(std_names_bt_mapper)} synonym{s} in Bionty:"
                f" {list(std_names_bt_mapper.keys())}"
            )
            warn_msg += (
                "\n   please add corresponding records via"
                f" `.from_values({list(std_names_bt_mapper.values())})`"
            )
            logger.warning(warn_msg)

        mapper.update(std_names_bt_mapper)
        result = pd.Series(std_names_db).replace(std_names_bt_mapper).tolist()
        return _return(
            result=result,
            mapper=mapper,
            return_mapper=return_mapper,
            return_str=return_str,
        )

    else:
        return _return(
            result=std_names_db,
            mapper=std_names_db,
            return_mapper=return_mapper,
            return_str=return_str,
        )


def _add_or_remove_synonyms(
    synonym: Union[str, Iterable],
    record: Registry,
    action: Literal["add", "remove"],
    force: bool = False,
    save: Optional[bool] = None,
):
    """Add or remove synonyms."""

    def check_synonyms_in_all_records(synonyms: Set[str], record: Registry):
        """Errors if input synonym is associated with other records in the DB."""
        import pandas as pd
        from IPython.display import display

        syns_all = (
            record.__class__.objects.exclude(synonyms="").exclude(synonyms=None).all()
        )
        if len(syns_all) == 0:
            return
        df = pd.DataFrame(syns_all.values())
        df["synonyms"] = df["synonyms"].str.split("|")
        df = df.explode("synonyms")
        matches_df = df[(df["synonyms"].isin(synonyms)) & (df["id"] != record.id)]
        if matches_df.shape[0] > 0:
            records_df = pd.DataFrame(syns_all.filter(id__in=matches_df["id"]).values())
            logger.error(
                f"input synonyms {matches_df['synonyms'].unique()} already associated"
                " with the following records:\n"
            )
            display(records_df)
            raise SystemExit(AssertionError)

    # passed synonyms
    # nothing happens when passing an empty string or list
    if isinstance(synonym, str):
        if len(synonym) == 0:
            return
        syn_new_set = set([synonym])
    else:
        if synonym == [""]:
            return
        syn_new_set = set(synonym)
    # nothing happens when passing an empty string or list
    if len(syn_new_set) == 0:
        return
    # because we use | as the separator
    if any(["|" in i for i in syn_new_set]):
        raise AssertionError("a synonym can't contain '|'!")

    # existing synonyms
    syns_exist = record.synonyms
    if syns_exist is None or len(syns_exist) == 0:
        syns_exist_set = set()
    else:
        syns_exist_set = set(syns_exist.split("|"))

    if action == "add":
        if not force:
            check_synonyms_in_all_records(syn_new_set, record)
        syns_exist_set.update(syn_new_set)
    elif action == "remove":
        syns_exist_set = syns_exist_set.difference(syn_new_set)

    if len(syns_exist_set) == 0:
        syns_str = None
    else:
        syns_str = "|".join(syns_exist_set)

    record.synonyms = syns_str

    if save is None:
        # if record is already in DB, save the changes to DB
        save = not record._state.adding
    if save:
        record.save()


def _check_synonyms_field_exist(record: Registry):
    try:
        record.__getattribute__("synonyms")
    except AttributeError:
        raise NotImplementedError(
            f"No synonyms field found in table {record.__class__.__name__}!"
        )


def _filter_query_based_on_species(
    orm: Union[Registry, QuerySet],
    species: Optional[Union[str, Registry]] = None,
    values_list_field: Optional[str] = None,
):
    import pandas as pd

    if values_list_field is None:
        records = orm.all() if isinstance(orm, QuerySet) else orm.objects.all()
    else:
        records = orm if isinstance(orm, QuerySet) else orm.objects
    if _has_species_field(orm):
        # here, we can safely import lnschema_bionty
        from lnschema_bionty._bionty import create_or_get_species_record

        species_record = create_or_get_species_record(
            species=species, orm=orm.model if isinstance(orm, QuerySet) else orm
        )
        if species_record is not None:
            records = records.filter(species__name=species_record.name)

    if values_list_field is None:
        return pd.DataFrame.from_records(records.values())
    else:
        return records.values_list(values_list_field, flat=True)


METHOD_NAMES = [
    "validate",
    "inspect",
    "standardize",
    "add_synonym",
    "remove_synonym",
    "set_abbr",
]

if _TESTING:  # type: ignore
    from inspect import signature

    SIGS = {
        name: signature(getattr(ValidationMixin, name))
        for name in METHOD_NAMES
        if not name.startswith("__")
    }

for name in METHOD_NAMES:
    attach_func_to_class_method(name, ValidationMixin, globals())
