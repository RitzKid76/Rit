from __future__ import annotations

from object.hash import Hash
from object.object import Object
from object.object_reference import ObjectReference


class Tree(Object):

    references: dict[Hash, ObjectReference]

    @classmethod
    def _from_data(cls, data: str) -> Tree:
        tree = cls()

        data = data.split(":")

        for data_reference in data:
            hash, name = Hash(data_reference[:40]), data_reference[40:]

            reference = ObjectReference(hash, name)
            tree.add_reference(reference)

    def _get_data(self):
        return ":".join(Tree._format_reference(reference) for reference in self.references)

    def add_reference(self, reference: ObjectReference):
        self.references[reference.hash] = reference

    @staticmethod
    def _format_reference(reference: Object) -> str:
        return f"{reference.get_hash()}{reference.name}"

    @staticmethod
    def type_label():
        return "t"
