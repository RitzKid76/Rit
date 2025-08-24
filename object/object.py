from __future__ import annotations

from abc import ABC, abstractmethod

from object.hash import Hash


class Object(ABC):

    name = None

    @classmethod
    def from_data(cls, raw_data: str) -> Object:
        from object.type.blob import Blob
        from object.type.tree import Tree

        type_label, data = raw_data[:1], raw_data[1:]

        if type_label == Blob.type_label():
            return Blob._from_data(data)
        elif type_label == Tree.type_label():
            return Tree._from_data(data)

        raise ValueError(f"unknown data type: {type_label}\nraw: {raw_data}")

    @classmethod
    @abstractmethod
    def _from_data(data: str) -> Object:
        pass

    def get_data(self) -> str:
        return f"{self.type_label()}{self._get_data()}"

    @abstractmethod
    def _get_data(self) -> str:
        pass

    def get_hash(self) -> Hash:
        Hash.from_contents(self.get_data())

    @staticmethod
    @abstractmethod
    def type_label() -> str:
        pass
