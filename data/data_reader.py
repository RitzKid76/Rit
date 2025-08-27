from __future__ import annotations

from data.byte_stream import ByteStream
from object.hash import Hash


class DataReader:

    def __init__(self, data: bytes):
        self.stream = ByteStream(data)

    def read_hash(self) -> Hash:
        return Hash.from_bytes(self.stream.read(20))

    def read_string(self) -> str:
        return self.stream.read_to_delimiter(b"\x00").decode("utf-8")

    def read_char(self) -> str:
        return chr(self.stream.read(1)[0])
    
    def read_int(self) -> int:
        return int(self.stream.read(4))

    def read_sector(self) -> bytes:
        length = self.read_int()
        return self.stream.read(length)

    def __len__(self) -> int:
        return len(self.stream)
    
    def __bool__(self) -> bool:
        return bool(self.stream)