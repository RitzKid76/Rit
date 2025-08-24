import gzip
import os

from object.hash import Hash
from object.object import Object
from object.type.blob import Blob


class Database:

    @staticmethod
    def _read_file(path: str) -> bytes:
        with open(path, "rb") as f:
            return f.read()

    @staticmethod
    def _write_file(path: str, contents: bytes):
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)

        with open(path, "wb") as f:
            f.write(contents)

    @staticmethod
    def _read_data(hash: Hash) -> str:
        path = Database._database_path(hash)

        compressed = Database._read_file(path)
        decompressed = gzip.decompress(compressed)

        return decompressed.decode("utf-8")

    @staticmethod
    def _write_data(contents: str | bytes):
        if isinstance(contents, bytes):
            contents = contents.decode("utf-8")

        hash = Hash.from_contents(contents)
        path = Database._database_path(hash)

        decompressed = contents.encode("utf-8")
        compressed = gzip.compress(decompressed)

        Database._write_file(path, compressed)

    @staticmethod
    def read_object(hash: Hash) -> Object:
        data = Database._read_data(hash)

        return Object.from_data(data)

    @staticmethod
    def write_object(object: Object):
        Database._write_data(object.get_data())

    @staticmethod
    def _database_path(hash: Hash) -> str:
        return f"database/{hash.database_path()}"

    @staticmethod
    def complete_hash(partial_hash: str) -> Hash:
        subset = partial_hash[:2]

        candidates = Database.get_subset(subset)
        matches = [h for h in candidates if h.hash.startswith(partial_hash)]

        match len(matches):
            case 0: raise ValueError(f"no hashes matching partial: {partial_hash}")
            case 1: return matches[0]
            case _: raise ValueError(f"Abiguous hash prefix: {partial_hash}, matches: {[str(h) for h in matches]}")
        
    @staticmethod
    def get_subset(subset: str) -> list[Hash]:
        output = []

        subset_path = f"database/{subset}"
        for path in os.listdir(subset_path):
            path = os.path.join(subset_path, path)
            output.append(Hash.from_path(path))

        return output

    @staticmethod
    def create_blob(path: str) -> Blob:
        pass