from base64 import b64decode, b64encode
from typing import Any, NamedTuple
from uuid import UUID


def encode_cursor(name: str, id: Any) -> str:
    return b64encode(f"{name}:{id}".encode("ascii")).decode("ascii")


class DecodedCursor(NamedTuple):
    name: str
    id: UUID


def decode_cursor(cursor: str) -> DecodedCursor:
    cursor_data = b64decode(cursor.encode("ascii")).decode("ascii")
    name, id = cursor_data.split(":", 1)
    return DecodedCursor(name=name, id=UUID(id))
