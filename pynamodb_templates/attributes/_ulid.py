from typing import TypeVar, AnyStr, Optional, Union, Callable, Any

from pynamodb import constants
from pynamodb.attributes import Attribute, NumberAttribute, BinaryAttribute
from pynamodb_templates.attributes.serializer import (
    NumberSerializeMixin,
    BinarySerializeMixin,
)
from ulid import ULID

_T = TypeVar("_T")

__all__ = ["UnicodeULIDAttribute", "NumberULIDAttribute", "BinaryULIDAttribute"]


class UnicodeULIDAttribute(Attribute[ULID]):
    """
    Unicode formatted ULID attribute
    """

    attr_type = constants.STRING

    def serialize(self, value: ULID) -> AnyStr:
        return super().serialize(str(value))

    def deserialize(self, value: AnyStr) -> ULID:
        return ULID.from_str(super().deserialize(value))


class NumberULIDAttribute(NumberSerializeMixin, Attribute[ULID]):
    """
    Number formatted ULID attribute
    """

    attr_type = constants.NUMBER

    def serialize(self, value: ULID) -> AnyStr:
        return super().serialize(int(value))

    def deserialize(self, value: AnyStr) -> ULID:
        return ULID.from_int(super().deserialize(value))


class BinaryULIDAttribute(BinarySerializeMixin, Attribute[ULID]):
    """
    Binary formatted ULID attribute
    """

    def serialize(self, value: ULID) -> bytes:
        return super().serialize(value.bytes)

    def deserialize(self, value: AnyStr) -> ULID:
        return ULID.from_bytes(super().deserialize(value))
