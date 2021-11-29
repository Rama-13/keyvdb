import json
from serializers import SerializationError, DeserializationError
from typing import Final


NULL_BYTE: Final = b"\x00"


class JSONSerializer:
    def dumps(self, obj: dict) -> bytes:
        try:
            return json.dumps(obj).encode() + NULL_BYTE
        except (ValueError, TypeError):
            raise SerializationError(obj)

    def loads(self, data: bytes) -> dict:
        data = data.split(NULL_BYTE, 1)[0]
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            raise DeserializationError(data)