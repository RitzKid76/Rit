from __future__ import annotations
import time

from data.data_reader import DataReader
from data.data_writer import DataWriter
from object.hash import Hash
from object.object import Object
from object.object_reference import ObjectReference


class Commit(Object):

    def __init__(self, tree: Hash | None = None, message: str = ""):
        self.tree = tree
        self.parents: list[ObjectReference] = []
        self.time: float = time.time()
        self.message = message

    @classmethod
    def deserialize(cls, reader: DataReader) -> Commit:
        commit = cls()

        commit.tree = reader.read_hash()
        commit.deserialize_parents(reader)
        commit.time = reader.read_float()
        commit.message = reader.read_string()

        return commit

    def serialize(self, writer: DataWriter):
        if self.tree is None:
            raise ValueError("no tree reference")

        writer.write_hash(self.tree)
        self.serialize_parents(writer)
        writer.write_float(self.time)
        writer.write_string(self.message)

    def deserialize_parents(self, reader: DataReader):
        sector = DataReader(reader.read_sector())

        while sector:
            self.add_parent(sector.read_reference())

    def serialize_parents(self, writer: DataWriter):
        sector = DataWriter()

        self.parents.sort(key=lambda r: str(r.hash))
        for parent in self.parents:
            sector.write_reference(parent)

        writer.write_sector(sector.bytes())

    def add_parent(self, parent: ObjectReference):
        self.parents.append(parent)

    def get_tree_reference(self) -> ObjectReference:
        if self.tree is None:
            raise ValueError("no tree reference")

        return ObjectReference(self.tree)

    @staticmethod
    def type() -> str:
        return "c"
