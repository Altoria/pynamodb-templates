"""
attributes from `lyft/pynamodb_attributes` packages

wrapping some attributes for full keyword arguments suggestion support
"""
from typing import Type, Tuple, TypeVar, Any, Optional, Union, Callable
from pynamodb_attributes import *
from datetime import datetime, timezone, timedelta

_T = TypeVar("_T")
T = TypeVar("T", bound=Tuple[Any, ...])
_DEFAULT_FIELD_DELIMITER = "::"


class UnicodeDelimitedTupleAttribute(UnicodeDelimitedTupleAttribute):
    def __init__(
        self,
        *,
        tuple_type: Type[T],
        delimiter: str = _DEFAULT_FIELD_DELIMITER,
        hash_key: bool = False,
        range_key: bool = False,
        null: Optional[bool] = None,
        default: Optional[Union[_T, Callable[..., _T]]] = None,
        default_for_new: Optional[Union[Any, Callable[..., _T]]] = None,
        attr_name: Optional[str] = None,
    ):

        super().__init__(
            tuple_type=tuple_type,
            delimiter=delimiter,
            hash_key=hash_key,
            range_key=range_key,
            null=null,
            default=default,
            default_for_new=default_for_new,
            attr_name=attr_name,
        )


class UUIDAttribute(UUIDAttribute):
    def __init__(
        self,
        *,
        remove_dashes: bool = False,
        hash_key: bool = False,
        range_key: bool = False,
        null: Optional[bool] = None,
        default: Optional[Union[_T, Callable[..., _T]]] = None,
        default_for_new: Optional[Union[Any, Callable[..., _T]]] = None,
        attr_name: Optional[str] = None,
    ):
        super().__init__(
            remove_dashes=remove_dashes,
            hash_key=hash_key,
            range_key=range_key,
            null=null,
            default=default,
            default_for_new=default_for_new,
            attr_name=attr_name,
        )


class UnicodeDatetimeAttribute(UnicodeDatetimeAttribute):
    def __init__(
        self,
        *,
        force_tz: bool = True,
        force_utc: bool = False,
        fmt: Optional[str] = None,
        hash_key: bool = False,
        range_key: bool = False,
        null: Optional[bool] = None,
        default: Optional[Union[_T, Callable[..., _T]]] = None,
        default_for_new: Optional[Union[Any, Callable[..., _T]]] = None,
        attr_name: Optional[str] = None,
    ):
        super().__init__(
            force_tz=force_tz,
            force_utc=force_utc,
            fmt=fmt,
            hash_key=hash_key,
            range_key=range_key,
            null=null,
            default=default,
            default_for_new=default_for_new,
            attr_name=attr_name,
        )


__all__ = [
    "FloatAttribute",
    "IntegerAttribute",
    "IntegerDateAttribute",
    # "IntegerEnumAttribute",
    "UnicodeDelimitedTupleAttribute",
    # "UnicodeEnumAttribute",
    "TimedeltaAttribute",
    "TimedeltaMsAttribute",
    "TimedeltaUsAttribute",
    "TimestampAttribute",
    "TimestampMsAttribute",
    "TimestampUsAttribute",
    "UUIDAttribute",
    "UnicodeDatetimeAttribute",
]
