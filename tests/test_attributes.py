from base64 import b64encode
from enum import Enum

import pytest
from pynamodb.attributes import DEFAULT_ENCODING
from pynamodb.constants import STRING, NUMBER, BINARY
from ulid import ULID

from pynamodb_templates.attributes import (
    IndexableBooleanAttribute,
    EnumNameAttribute,
    InteagerEnumAttribute,
    UnicodeEnumAttribute,
    UnicodeULIDAttribute,
    NumberULIDAttribute,
    BinaryULIDAttribute,
)


# from ulid import ULID


class IntEnum(int, Enum):
    zero = 0
    one = 1
    two = 2


class FloatEnum(float, Enum):
    one = 1.0
    two = 2.0


class StrEnum(Enum):
    a = "a"
    b = "b"


class StrIntEnum(Enum):
    zero = "0"
    one = "1"


class MutualEnum(Enum):
    one = 1
    two = "2"
    phi = 3.14159


class TestIndexableBooleanAttribute:
    """
    Tests boolean attributes
    """

    def test_indexable_boolean_attribute(self):
        """
        BooleanAttribute.default
        """
        attr = IndexableBooleanAttribute(default=True)
        assert attr.attr_type == NUMBER
        assert attr.default is True

    def test_indexable_boolean_serialize(self):
        """
        IndexableBooleanAttribute.serialize
        """
        attr = IndexableBooleanAttribute()
        assert attr.serialize(True) == "1"
        assert attr.serialize(False) == "0"

    def test_indexable_boolean_deserialize(self):
        """
        IndexableBooleanAttribute.deserialize
        """
        attr = IndexableBooleanAttribute()
        assert attr.deserialize("1") is True
        assert attr.deserialize("0") is False


class TestEnumNameAttribute:
    """
    Test EnumNameAttribute
    """

    def test_enum_name_attribute(self):
        attr = EnumNameAttribute(enum_type=StrEnum)
        attr = EnumNameAttribute(enum_type=IntEnum)
        attr = EnumNameAttribute(enum_type=MutualEnum)
        assert attr.attr_type == STRING

        attr = EnumNameAttribute(enum_type=MutualEnum, default=MutualEnum.one)

        assert attr.default == MutualEnum.one

    def test_enum_name_serialize(self):
        attr = EnumNameAttribute(enum_type=MutualEnum)
        assert attr.serialize(MutualEnum.one) == "one"
        assert attr.serialize(MutualEnum.phi) == "phi"

    def test_enum_name_deserialize(self):
        attr = EnumNameAttribute(enum_type=MutualEnum)
        assert attr.deserialize("one") == MutualEnum.one
        assert attr.deserialize("phi") == MutualEnum.phi


class TestInteagerEnumAttribute:
    """
    Test InteagerEnumAttribute
    """

    def test_inteager_enum_attribute(self):
        attr = InteagerEnumAttribute(enum_type=IntEnum)
        assert attr.attr_type == NUMBER

        attr = InteagerEnumAttribute(enum_type=IntEnum, default=IntEnum.one)
        assert attr.default == IntEnum.one

    def test_inteager_enum_serialize(self):
        attr = InteagerEnumAttribute(enum_type=IntEnum)
        assert attr.serialize(IntEnum.zero) == "0"
        assert attr.serialize(IntEnum.one) == "1"

    def test_inteager_enum_deserialize(self):
        attr = InteagerEnumAttribute(enum_type=IntEnum)
        assert attr.deserialize("1") == IntEnum.one
        assert attr.deserialize("0") == IntEnum.zero

    def test_inteager_enum_type_error(self):
        with pytest.raises(TypeError):
            attr = InteagerEnumAttribute(enum_type=FloatEnum)
        with pytest.raises(TypeError):
            attr = InteagerEnumAttribute(enum_type=StrIntEnum)


class TestUnicodeEnumAttribute:
    """
    Test UnicodeEnumAttribute
    """

    def test_unicode_enum_attribute(self):
        attr = UnicodeEnumAttribute(enum_type=StrEnum)
        assert attr.attr_type == STRING

        attr = UnicodeEnumAttribute(enum_type=StrEnum, default=StrEnum.a)
        assert attr.default == StrEnum.a

    def test_unicode_enum_serialize(self):
        attr = UnicodeEnumAttribute(enum_type=StrEnum)
        assert attr.serialize(StrEnum.a) == "a"
        assert attr.serialize(StrEnum.b) == "b"

    def test_unicode_enum_deserialize(self):
        attr = UnicodeEnumAttribute(enum_type=StrEnum)
        assert attr.deserialize("a") == StrEnum.a
        assert attr.deserialize("b") == StrEnum.b

    def test_inteager_enum_type_error(self):
        with pytest.raises(TypeError):
            attr = InteagerEnumAttribute(enum_type=FloatEnum)
        with pytest.raises(TypeError):
            attr = InteagerEnumAttribute(enum_type=StrIntEnum)


class TestUnicodeULIDAttribute:
    ULID_ZERO = ULID.from_str("0000000000FYFV2P0FWPC65H57")

    def test_unicode_ulid_attribute(self):
        _rand_ulid = ULID()

        attr = UnicodeULIDAttribute()
        assert attr.attr_type == STRING

        attr = UnicodeULIDAttribute(default=_rand_ulid)
        assert attr.default == _rand_ulid

    def test_unicode_ulid_serialize(self):
        _rand_ulid = ULID()

        attr = UnicodeULIDAttribute()
        assert attr.serialize(_rand_ulid) == str(_rand_ulid)
        assert attr.serialize(self.ULID_ZERO) == str(self.ULID_ZERO)

    def test_unicode_ulid_deserialize(self):
        _rand_uild = ULID()

        attr = UnicodeULIDAttribute()
        assert attr.deserialize(str(_rand_uild)) == _rand_uild
        assert attr.deserialize(str(self.ULID_ZERO)) == self.ULID_ZERO

    def test_unicode_uild_roundtrip(self):
        _rand_uild = ULID()

        attr = UnicodeULIDAttribute()
        assert attr.deserialize(attr.serialize(_rand_uild)) == _rand_uild
        assert attr.deserialize(attr.serialize(self.ULID_ZERO)) == self.ULID_ZERO


class TestNumberULIDAttribute:
    ULID_ZERO = ULID.from_str("0000000000FYFV2P0FWPC65H57")

    def test_number_ulid_attribute(self):
        _rand_ulid = ULID()

        attr = NumberULIDAttribute()
        assert attr.attr_type == NUMBER

        attr = NumberULIDAttribute(default=_rand_ulid)
        assert attr.default == _rand_ulid

    def test_number_ulid_serialize(self):
        _rand_ulid = ULID()

        attr = NumberULIDAttribute()
        assert attr.serialize(_rand_ulid) == str(int(_rand_ulid))
        assert attr.serialize(self.ULID_ZERO) == str(int(self.ULID_ZERO))

    def test_number_ulid_deserialize(self):
        _rand_uild = ULID()

        attr = NumberULIDAttribute()
        assert attr.deserialize(str(int(_rand_uild))) == _rand_uild
        assert attr.deserialize(str(int(self.ULID_ZERO))) == self.ULID_ZERO

    def test_unicode_uild_roundtrip(self):
        _rand_uild = ULID()

        attr = NumberULIDAttribute()
        assert attr.deserialize(attr.serialize(_rand_uild)) == _rand_uild
        assert attr.deserialize(attr.serialize(self.ULID_ZERO)) == self.ULID_ZERO


class TestBinaryULIDAttribute:
    ULID_ZERO: ULID = ULID.from_str("0000000000FYFV2P0FWPC65H57")

    def test_binary_ulid_attribute(self):
        _rand_ulid = ULID()

        attr = BinaryULIDAttribute()
        assert attr.attr_type == BINARY

        attr = BinaryULIDAttribute(default=_rand_ulid)
        assert attr.default == _rand_ulid

    def test_binary_ulid_serialize(self):
        _rand_ulid = ULID()

        attr = BinaryULIDAttribute()
        assert attr.serialize(_rand_ulid) == b64encode(_rand_ulid.bytes).decode(
            DEFAULT_ENCODING
        )
        assert attr.serialize(self.ULID_ZERO) == b64encode(self.ULID_ZERO.bytes).decode(
            DEFAULT_ENCODING
        )

    def test_binary_ulid_deserialize(self):
        _rand_uild = ULID()

        attr = BinaryULIDAttribute()
        assert (
            attr.deserialize(b64encode(_rand_uild.bytes).decode(DEFAULT_ENCODING))
            == _rand_uild
        )
        assert (
            attr.deserialize(b64encode(self.ULID_ZERO.bytes).decode(DEFAULT_ENCODING))
            == self.ULID_ZERO
        )

    def test_unicode_uild_roundtrip(self):
        _rand_uild = ULID()

        attr = BinaryULIDAttribute()
        assert attr.deserialize(attr.serialize(_rand_uild)) == _rand_uild
        assert attr.deserialize(attr.serialize(self.ULID_ZERO)) == self.ULID_ZERO
