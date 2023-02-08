from abc import ABCMeta
from enum import Enum
from typing import Type, TypeVar, AnyStr, Optional, Callable, Union, Any

from pynamodb import constants
from pynamodb.attributes import Attribute

from pynamodb_templates.attributes.serializer import NumberSerializeMixin

__all__ = ["EnumNameAttribute", "InteagerEnumAttribute", "UnicodeEnumAttribute"]

_T = TypeVar("_T")


def is_unique(obj: Type[Enum]):
    v = [e.value for e in obj]
    if len(v) == len(set(v)):
        return True
    return False


class EnumAttributeBase(Attribute[Enum], metaclass=ABCMeta):
    attr_type: str
    attr_type_check_by: Optional[Any] = None
    _enum_save_name: bool

    def __init__(
        self,
        enum_type: Type[Enum],
        hash_key: bool = False,
        range_key: bool = False,
        null: Optional[bool] = None,
        default: Optional[Union[_T, Callable[..., _T]]] = None,
        default_for_new: Optional[Union[Any, Callable[..., _T]]] = None,
        attr_name: Optional[str] = None,
    ) -> None:
        super().__init__(
            hash_key=hash_key,
            range_key=range_key,
            null=null,
            default=default,
            default_for_new=default_for_new,
            attr_name=attr_name,
        )

        self.enum_type = enum_type
        if not self._enum_save_name:
            assert is_unique(enum_type), "all values must be unique in enum object"
        if self.attr_type_check_by:
            for e in enum_type:
                if not isinstance(e.value, self.attr_type_check_by):
                    raise TypeError(
                        f"`{str(self.attr_type_check_by)}` type expected, "
                        f"but `type({type(e.value)})` type from name `{e.name}`"
                    )

    def __getattr__(self, item):
        if item in self.enum_type.__members__:
            return self.enum_type[item]
        raise AttributeError(item)

    def serialize(self, value: Enum):
        if self._enum_save_name:
            v = value.name
        else:
            v = value.value
        return super().serialize(v)

    def deserialize(self, value: str) -> Enum:
        if self._enum_save_name:
            return self.enum_type[super().deserialize(value)]
        return self.enum_type(super().deserialize(value))

    @property
    def enum_names(self):
        return [e.name for e in self.enum_type]

    @property
    def enum_values(self):
        return [e.value for e in self.enum_type]


class EnumNameAttribute(EnumAttributeBase):
    """
    Unicode formatted enum's name attributes
    """

    attr_type = constants.STRING
    _enum_save_name = True


class UnicodeEnumAttribute(EnumAttributeBase):
    """
    Unicode formatted enum value attributes
    """

    attr_type = constants.STRING
    attr_type_check_by = str

    _enum_save_name = False


class InteagerEnumAttribute(NumberSerializeMixin, EnumAttributeBase):
    """
    Number formatted enum value attributes
    """

    attr_type = constants.NUMBER
    attr_type_check_by = int

    _enum_save_name = False

    def serialize(self, value: Enum) -> AnyStr:
        return super().serialize(value.value)

    def deserialize(self, value: AnyStr) -> Enum:
        return self.enum_type(super().deserialize(value))
