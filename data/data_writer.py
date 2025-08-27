from data.byte_stream import ByteStream
from object.hash import Hash


class DataWriter:

    def __init__(self):
        self.stream = ByteStream()

    def write_hash(self, hash: Hash):
        self.stream.write(hash.to_bytes())

    def write_string(self, string: str):
        self.stream.write(string.encode("utf-8") + b"\x00")

    def write_char(self, char: str):
        self.stream.write(bytes([ord(char)]))

    def write_int(self, int: int):
        self.stream.write(bytes(int))

    def write_sector(self, sector: bytes):
        self.stream.write(bytes([len(sector)]))
        self.stream.write(sector)

    def bytes(self):
        return self.stream.bytes()

    def __len__(self) -> int:
        return len(self.stream)
    
    def __bool__(self) -> bool:
        return bool(self.stream)