from __future__ import annotations

from data.data_reader import DataReader
from data.data_writer import DataWriter
from object.object import Object


class Blob(Object):

    def __init__(self, contents: str):
        self.contents = contents

    @classmethod
    def deserialize(cls, reader: DataReader) -> Blob:
        return cls(reader.read_string())

    def serialize(self, writer: DataWriter):
        writer.write_string(self.contents)

    @staticmethod
    def type() -> str:
        return "b"
