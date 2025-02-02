from __future__ import annotations

from typing import TYPE_CHECKING

import lamindb_setup as ln_setup
import numpy as np
from lamin_utils import logger
from lamindb_setup.core._docs import doc_args
from lamindb_setup.core.hashing import hash_set

from lamindb.base import ids
from lamindb.base.types import FieldAttr, ListLike
from lamindb.models import Feature, Record, Schema

from ._feature import convert_pandas_dtype_to_lamin_dtype
from ._record import init_self_from_db, update_attributes
from ._utils import attach_func_to_class_method
from .core.relations import (
    dict_related_model_to_related_name,
    get_related_name,
)
from .errors import ValidationError

if TYPE_CHECKING:
    from collections.abc import Iterable

    import pandas as pd

    from ._query_set import QuerySet

NUMBER_TYPE = "num"
DICT_KEYS_TYPE = type({}.keys())  # type: ignore


def validate_features(features: list[Record]) -> Record:
    """Validate and return feature type."""
    try:
        if len(features) == 0:
            raise ValueError("Provide list of features with at least one element")
    except TypeError:
        raise ValueError(
            "Please pass a ListLike of features, not a single feature"
        ) from None
    if not hasattr(features, "__getitem__"):
        raise TypeError("features has to be list-like")
    if not isinstance(features[0], Record):
        raise TypeError(
            "features has to store feature records! use .from_values() otherwise"
        )
    feature_types = {feature.__class__ for feature in features}
    if len(feature_types) > 1:
        raise TypeError("schema can only contain a single type")
    for feature in features:
        if feature._state.adding:
            raise ValueError("Can only construct feature sets from validated features")
    return next(iter(feature_types))  # return value in set of cardinality 1


def __init__(self, *args, **kwargs):
    if len(args) == len(self._meta.concrete_fields):
        super(Schema, self).__init__(*args, **kwargs)
        return None
    # now we proceed with the user-facing constructor
    if len(args) > 1:
        raise ValueError("Only one non-keyword arg allowed: features")

    # Extract primary constructor arguments
    features: Iterable[Record] = kwargs.pop("features") if len(args) == 0 else args[0]

    # Extract all possible field values with their defaults
    name: str | None = kwargs.pop("name", None)
    description: str | None = kwargs.pop("description", None)
    dtype: str | None = kwargs.pop("dtype", None)
    itype: str | None = kwargs.pop("itype", None)
    type: Feature | None = kwargs.pop("type", None)
    is_type: bool = kwargs.pop("is_type", False)
    otype: str | None = kwargs.pop("otype", None)
    minimal_set: bool = kwargs.pop("minimal_set", True)
    ordered_set: bool = kwargs.pop("ordered_set", False)
    maximal_set: bool = kwargs.pop("maximal_set", False)
    composite: Schema | None = kwargs.pop("composite", None)
    slot: str | None = kwargs.pop("slot", None)
    validated_by: Schema | None = kwargs.pop("validated_by", None)

    # Check for unexpected keyword arguments
    if kwargs:
        raise ValueError(
            f"Unexpected keyword arguments: {', '.join(kwargs.keys())}\n"
            "Valid arguments are: features, description, dtype, itype, type, "
            "is_type, otype, minimal_set, ordered_set, maximal_set, composite, "
            "slot, validated_by"
        )

    # now code
    features_registry = validate_features(features)
    if dtype is None:
        dtype = None if features_registry == Feature else NUMBER_TYPE
    n_features = len(features)
    hash = hash_set({feature.uid for feature in features})
    validated_kwargs = {
        "name": name,
        "description": description,
        "type": type,
        "dtype": get_type_str(dtype),
        "is_type": is_type,
        "otype": otype,
        "n": n_features,
        "itype": (
            features_registry.__get_name_with_module__() if itype is None else itype
        ),
        "hash": hash,
        "minimal_set": minimal_set,
        "ordered_set": ordered_set,
        "maximal_set": maximal_set,
        "composite": composite,
        "slot": slot,
        "validated_by": validated_by,
    }
    # compute hash
    schema = Schema.filter(hash=hash).one_or_none()
    if schema is not None:
        logger.important(f"returning existing schema with same hash: {schema}")
        init_self_from_db(self, schema)
        update_attributes(self, validated_kwargs)
        return None
    else:
        self._features = (get_related_name(features_registry), features)
        validated_kwargs["uid"] = ids.base62_20()
        super(Schema, self).__init__(**validated_kwargs)


@doc_args(Schema.save.__doc__)
def save(self, *args, **kwargs) -> Schema:
    """{}"""  # noqa: D415
    super(Schema, self).save(*args, **kwargs)
    if hasattr(self, "_features"):
        related_name, records = self._features
        # only the following method preserves the order
        # .set() does not preserve the order but orders by
        # the feature primary key
        through_model = getattr(self, related_name).through
        related_model_split = self.itype.split(".")
        if len(related_model_split) == 1:
            related_field = related_model_split[0].lower()
        else:
            related_field = related_model_split[1].lower()
        related_field_id = f"{related_field}_id"
        links = [
            through_model(**{"schema_id": self.id, related_field_id: record.id})
            for record in records
        ]
        through_model.objects.bulk_create(links, ignore_conflicts=True)
    return self


def get_type_str(dtype: str | None) -> str | None:
    if dtype is not None:
        type_str = dtype.__name__ if not isinstance(dtype, str) else dtype  # type: ignore
    else:
        type_str = None
    return type_str


@classmethod  # type:ignore
@doc_args(Schema.from_values.__doc__)
def from_values(
    cls,
    values: ListLike,
    field: FieldAttr = Feature.name,
    type: str | None = None,
    name: str | None = None,
    mute: bool = False,
    organism: Record | str | None = None,
    source: Record | None = None,
    raise_validation_error: bool = True,
) -> Schema:
    """{}"""  # noqa: D415
    if not isinstance(field, FieldAttr):
        raise TypeError("Argument `field` must be a Record field, e.g., `Feature.name`")
    if len(values) == 0:
        raise ValueError("Provide a list of at least one value")
    if isinstance(values, DICT_KEYS_TYPE):
        values = list(values)
    registry = field.field.model
    if registry != Feature and type is None:
        type = NUMBER_TYPE
        logger.debug("setting feature set to 'number'")
    validated = registry.validate(values, field=field, mute=mute, organism=organism)
    values_array = np.array(values)
    validated_values = values_array[validated]
    if validated.sum() != len(values):
        not_validated_values = values_array[~validated]
        msg = (
            f"These values could not be validated: {not_validated_values.tolist()}\n"
            f"If there are no typos, add them to their registry: {registry.__name__}"
        )
        if raise_validation_error:
            raise ValidationError(msg)
        elif len(validated_values) == 0:
            return None  # temporarily return None here
    validated_features = registry.from_values(
        validated_values,
        field=field,
        organism=organism,
        source=source,
    )
    schema = Schema(
        features=validated_features,
        name=name,
        dtype=get_type_str(type),
    )
    return schema


@classmethod  # type:ignore
@doc_args(Schema.from_df.__doc__)
def from_df(
    cls,
    df: pd.DataFrame,
    field: FieldAttr = Feature.name,
    name: str | None = None,
    mute: bool = False,
    organism: Record | str | None = None,
    source: Record | None = None,
) -> Schema | None:
    """{}"""  # noqa: D415
    registry = field.field.model
    validated = registry.validate(df.columns, field=field, mute=mute, organism=organism)
    if validated.sum() == 0:
        if mute is True:
            logger.warning("no validated features, skip creating feature set")
        return None
    if registry == Feature:
        validated_features = Feature.from_values(  # type: ignore
            df.columns, field=field, organism=organism
        )
        schema = Schema(validated_features, name=name, dtype=None)
    else:
        dtypes = [col.dtype for (_, col) in df.loc[:, validated].items()]
        if len(set(dtypes)) != 1:
            raise ValueError(f"data types are heterogeneous: {set(dtypes)}")
        dtype = convert_pandas_dtype_to_lamin_dtype(dtypes[0])
        validated_features = registry.from_values(
            df.columns[validated],
            field=field,
            organism=organism,
            source=source,
        )
        schema = Schema(
            features=validated_features,
            name=name,
            dtype=get_type_str(dtype),
        )
    return schema


@property  # type: ignore
@doc_args(Schema.members.__doc__)
def members(self) -> QuerySet:
    """{}"""  # noqa: D415
    if self._state.adding:
        # this should return a queryset and not a list...
        # need to fix this
        return self._features[1]
    related_name = self._get_related_name()
    if related_name is None:
        related_name = "features"
    return self.__getattribute__(related_name).order_by("links_schema__id")


def _get_related_name(self: Schema) -> str:
    related_models = dict_related_model_to_related_name(self, instance=self._state.db)
    related_name = related_models.get(self.itype)
    return related_name


METHOD_NAMES = [
    "__init__",
    "from_values",
    "from_df",
    "save",
]

if ln_setup._TESTING:
    from inspect import signature

    SIGS = {
        name: signature(getattr(Schema, name))
        for name in METHOD_NAMES
        if name != "__init__"
    }

for name in METHOD_NAMES:
    attach_func_to_class_method(name, Schema, globals())

Schema.members = members  # type: ignore
Schema._get_related_name = _get_related_name
Schema.feature_sets = Schema._artifacts_m2m  # backward compat
