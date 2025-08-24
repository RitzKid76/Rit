from __future__ import annotations

from object.hash import Hash


class ObjectReference:

    def __init__(self, hash: Hash, name: str):
        self.name = name
        self.hash = hash