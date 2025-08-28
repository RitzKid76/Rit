from __future__ import annotations

import struct
from typing import TYPE_CHECKING

from data.byte_stream import ByteStream
from object.hash import Hash

if TYPE_CHECKING:
    from object.object_reference import ObjectReference

class DataWriter:

    def __init__(self, stream: ByteStream | None = None):
        self.stream = ByteStream() if stream is None else stream 

    def write_reference(self, reference: ObjectReference):
        self.write_hash(reference.hash)
        self.write_string(reference.name)

    def write_hash(self, hash: Hash):
        self.stream.write(hash.to_bytes())

    def write_string(self, string: str):
        self.stream.write(string.encode("utf-8") + b"\x00")

    def write_char(self, char: str):
        self.stream.write(bytes([ord(char)]))

    def write_int(self, int: int):
        self.stream.write(int.to_bytes(4, "big"))

    def write_float(self, float: float):
        self.stream.write(struct.pack('>d', float))

    def write_sector(self, sector: bytes):
        self.write_int(len(sector))
        self.stream.write(sector)

    def bytes(self):
        return self.stream.bytes()

    def __len__(self) -> int:
        return len(self.stream)
    
    def __bool__(self) -> bool:
        return bool(self.stream)