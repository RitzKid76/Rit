from __future__ import annotations

from object.hash import Hash
from object.object import Object
from object.object_reference import ObjectReference


class Tree(Object):

    def __init__(self):
        self.references: list[ObjectReference] = []

    @classmethod
    def _from_data(cls, data: str) -> Tree:
        tree = cls()

        data = data.split(":")

        for data_reference in data:
            hash, name = Hash(data_reference[:40]), data_reference[40:]

            reference = ObjectReference(hash, name)
            tree.add_reference(reference)

        return tree

    def _get_data(self):
        hash_paired_formats = []
        for reference in self.references:
            hash_paired_formats.append((
                reference.hash,
                Tree._format_reference(reference))
            )

        hash_paired_formats.sort(key=lambda p: p[1])

        return ":".join(hash_paired[1] for hash_paired in hash_paired_formats)

    def add_reference(self, reference: ObjectReference):
        self.references.append(reference)

    @staticmethod
    def _format_reference(reference: ObjectReference) -> str:
        return f"{reference.hash}{reference.name}"

    @staticmethod
    def type_label():
        return "t"
