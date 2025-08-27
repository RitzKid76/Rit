from __future__ import annotations

from data.data_reader import DataReader
from data.data_writer import DataWriter
from object.object import Object
from object.object_reference import ObjectReference


class Tree(Object):

    def __init__(self):
        self.references: list[ObjectReference] = []

    @classmethod
    def deserialize(cls, reader: DataReader) -> Tree:
        tree = cls()

        while reader:
            tree.add_reference(Tree.deserialize_reference(reader))

        return tree

    def serialize(self, writer: DataWriter):
        self.references.sort(key=lambda r: str(r.hash))

        for reference in self.references:
            Tree.serialize_reference(writer, reference)

    def add_reference(self, reference: ObjectReference):
        self.references.append(reference)

    @staticmethod
    def deserialize_reference(reader: DataReader) -> ObjectReference:
        hash = reader.read_hash()
        name = reader.read_string()

        return ObjectReference(hash, name)

    @staticmethod
    def serialize_reference(writer: DataWriter, reference: ObjectReference):
        writer.write_hash(reference.hash)
        writer.write_string(reference.name)

    @staticmethod
    def type():
        return "t"
