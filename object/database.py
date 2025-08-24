import gzip
import os

from object.hash import Hash
from object.object import Object
from object.object_reference import ObjectReference
from object.type.blob import Blob
from object.type.tree import Tree
from typing import cast


class Database:

    @staticmethod
    def str_to_bytes(data: str) -> bytes:
        return data.encode("utf-8")

    @staticmethod
    def bytes_to_str(data: bytes) -> str:
        return data.decode("utf-8")

    @staticmethod
    def _create_folder(path: str):
        directory = os.path.dirname(path)
        os.makedirs(directory, exist_ok=True)

    @staticmethod
    def _read_file(path: str) -> bytes:
        with open(path, "rb") as f:
            return f.read()

    @staticmethod
    def _write_file(path: str, contents: str | bytes):
        Database._create_folder(path)

        if isinstance(contents, str):
            contents = Database.str_to_bytes(contents)

        with open(path, "wb") as f:
            f.write(contents)

    @staticmethod
    def _read_data(hash: Hash) -> str:
        path = Database._database_path(hash)

        compressed = Database._read_file(path)
        decompressed = gzip.decompress(compressed)

        return Database.bytes_to_str(decompressed)

    @staticmethod
    def _write_data(contents: str | bytes):
        if isinstance(contents, bytes):
            contents = Database.bytes_to_str(contents)

        hash = Hash.from_contents(contents)
        path = Database._database_path(hash)

        decompressed = Database.str_to_bytes(contents)
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
    def _is_dir(path: str) -> bool:
        return os.path.isdir(path)

    @staticmethod
    def _create_blob_reference(path: str) -> ObjectReference:
        contents = Database.bytes_to_str(Database._read_file(path))
        blob = Blob(contents)
        name = os.path.basename(path)

        return ObjectReference.from_object(blob, name)

    @staticmethod
    def _create_tree_reference(path: str) -> ObjectReference:
        if not Database._is_dir(path):
            return Database._create_blob_reference(path)

        tree = Tree()
        name = os.path.basename(path)

        for dir in os.listdir(path):
            dir = os.path.join(path, dir)

            reference = Database._create_tree_reference(dir)
            tree.add_reference(reference)

        tree_reference = ObjectReference.from_object(tree, name)
        return tree_reference

    @staticmethod
    def _write_reference(reference: ObjectReference):
        object = reference.get_object()
        Database.write_object(object)

        if isinstance(object, Blob):
            return

        tree = cast(Tree, object)
        for reference in tree.references:
            Database._write_reference(reference)

    @staticmethod
    def store(path: str):
        Database._write_reference(Database._create_tree_reference(path))

    @staticmethod
    def _load_reference(reference: ObjectReference, path: str = "test"):
        object = reference.get_object()
        path = os.path.join(path, reference.name)

        if isinstance(object, Blob):
            Database._write_file(path, object.contents)
            return

        tree = cast(Tree, object)
        for reference in tree.references:
            Database._load_reference(reference, path)

    @staticmethod
    def load(hash: Hash):
        object = Database.read_object(hash)

        if isinstance(object, Blob):
            raise ValueError(
                f"hash {hash} points to a blob. file name is not recoverable")

        tree = cast(Tree, object)
        for reference in tree.references:
            Database._load_reference(reference)
