from __future__ import annotations

from abc import ABC, abstractmethod

from data.data_reader import DataReader
from data.data_writer import DataWriter
from object.hash import Hash


class Object(ABC):

    @classmethod
    def from_reader(cls, reader: DataReader) -> Object:
        from object.type.blob import Blob
        from object.type.tree import Tree

        from data.file_manager import FileManager

        type = reader.read_char()

        if type == Blob.type():
            return Blob.deserialize(reader)
        elif type == Tree.type():
            return Tree.deserialize(reader)

        raise ValueError(f"unknown data type: {type}")

    @abstractmethod
    def deserialize(self, data: DataReader) -> Object:
        pass

    def get_data(self) -> bytes:
        writer = DataWriter()

        writer.write_char(self.type())
        self.serialize(writer)

        return writer.bytes()

    @abstractmethod
    def serialize(self, writer: DataWriter):
        pass

    def get_hash(self) -> Hash:
        return Hash.from_contents(self.get_data())

    @staticmethod
    @abstractmethod
    def type() -> str:
        pass
