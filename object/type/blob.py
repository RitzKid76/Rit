from __future__ import annotations

from object.object import Object


class Blob(Object):

    def __init__(self, contents: str):
        self.contents = contents

    @classmethod
    def _from_data(cls, data: str) -> Blob:
        return cls(data)

    def _get_data(self):
        return self.contents
    
    @staticmethod
    def type_label() -> str:
        return "b"
