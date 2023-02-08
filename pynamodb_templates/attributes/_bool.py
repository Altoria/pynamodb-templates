from typing import TypeVar

from pynamodb.attributes import Attribute

from pynamodb_templates.attributes.serializer import NumberSerializeMixin

_T = TypeVar("_T")

__all__ = ["IndexableBooleanAttribute"]


class IndexableBooleanAttribute(NumberSerializeMixin, Attribute[bool]):
    """
    Indexable Boolean Attribute using Number Field
    """

    def serialize(self, value):
        if value is not None:
            value = int(value)
        return super().serialize(value)

    def deserialize(self, value):
        value = super().deserialize(value)
        if value is None:
            return
        else:
            return bool(value)
