from __future__ import annotations

from object.hash import Hash
from object.object import Object


class ObjectReference:

    def __init__(self, hash: Hash, name: str):
        self.name = name
        self.hash = hash
        self.object: Object | None = None

    @classmethod
    def from_object(cls, object: Object, name: str) -> ObjectReference:
        hash = object.get_hash()

        reference = ObjectReference(hash, name)
        reference.object = object

        return reference

    def get_object(self) -> Object:
        if self.object is not None:
            return self.object

        try:
            from object.database import Database
            return Database.read_object(self.hash)
        except FileNotFoundError:
            raise AttributeError(f"reference to [{self.hash}] does not contain an object")