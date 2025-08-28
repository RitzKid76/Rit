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
            tree.add_reference(reader.read_reference())

        return tree

    def serialize(self, writer: DataWriter):
        self.references.sort(key=lambda r: str(r.hash))

        for reference in self.references:
            writer.write_reference(reference)

    def add_reference(self, reference: ObjectReference):
        self.references.append(reference)

    @staticmethod
    def type() -> str:
        return "t"
