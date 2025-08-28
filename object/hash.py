from __future__ import annotations

import hashlib
import re


class Hash:

    def __init__(self, hash: str):
        self.hash = hash

    @classmethod
    def from_partial(cls, hash: str) -> Hash:
        if Hash.is_hash(hash):
            return cls(hash)

        if not Hash.is_hash_like(hash):
            raise ValueError(f"{hash} is not hash like")

        from object.database import Database
        return Database.complete_hash(hash)

    @classmethod
    def from_contents(cls, contents: bytes) -> Hash:
        return cls(hashlib.sha1(contents).hexdigest())

    @classmethod
    def from_path(cls, path: str) -> Hash:
        pattern = r".*([0-9a-f]{2})\\([0-9a-f]{38})"
        if match := re.match(pattern, path):
            a, b = match.groups()
            return cls(a + b)

        raise ValueError(f"No hash found in {path}")
    
    @classmethod
    def from_bytes(cls, bytes: bytes) -> Hash:
        return Hash(bytes.hex())
    
    def to_bytes(self) -> bytes:
        return bytes.fromhex(self.hash)

    def database_path(self) -> str:
        folder = self.hash[:2]
        file = self.hash[2:]

        return f"{folder}/{file}"

    @staticmethod
    def is_hash(hash: str) -> bool:
        if not Hash.is_hash_like(hash):
            return False

        return len(hash) == 40

    @staticmethod
    def is_hash_like(hash: str) -> bool:
        if len(hash) < 3:
            return False

        pattern = r"[0-9a-f]+"
        return bool(re.match(pattern, hash))

    def __str__(self) -> str:
        return self.hash
