from __future__ import annotations

import struct
from typing import TYPE_CHECKING

from data.byte_stream import ByteStream
from object.hash import Hash

if TYPE_CHECKING:
    from object.object_reference import ObjectReference


class DataReader:

    def __init__(self, data: bytes | ByteStream):
        self.stream = data if isinstance(data, ByteStream) else ByteStream(data)

    def read_reference(self) -> ObjectReference:
        from object.object_reference import ObjectReference

        hash = self.read_hash()
        name = self.read_string()

        return ObjectReference(hash, name)

    def read_hash(self) -> Hash:
        return Hash.from_bytes(self.stream.read(20))

    def read_string(self) -> str:
        return self.stream.read_to_delimiter(b"\x00").decode("utf-8")

    def read_char(self) -> str:
        return chr(self.stream.read(1)[0])
    
    def read_int(self) -> int:
        return int.from_bytes(self.stream.read(4), "big")
    
    def read_float(self) -> float:
        return struct.unpack('>d', self.stream.read(8))[0]

    def read_sector(self) -> bytes:
        length = self.read_int()
        return self.stream.read(length)

    def __len__(self) -> int:
        return len(self.stream)
    
    def __bool__(self) -> bool:
        return bool(self.stream)