import json
from base64 import b64encode, b64decode

import pynamodb.constants
from pynamodb.attributes import DEFAULT_ENCODING


class NumberSerializeMixin:
    attr_type = pynamodb.constants.NUMBER

    def serialize(self, value):
        """
        Encode numbers as JSON
        """
        return json.dumps(value)

    def deserialize(self, value):
        """
        Decode numbers from JSON
        """
        return json.loads(value)


class BinarySerializeMixin:
    attr_type = pynamodb.constants.BINARY

    def serialize(self, value):
        """
        Returns a base64 encoded binary string
        """
        return b64encode(value).decode(DEFAULT_ENCODING)

    def deserialize(self, value):
        """
        Returns a decoded byte string from a base64 encoded value
        """
        return b64decode(value)
