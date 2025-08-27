import gzip
import os

from data.data_reader import DataReader
from data.file_manager import FileManager
from object.hash import Hash
from object.object import Object
from object.object_reference import ObjectReference
from object.type.blob import Blob
from object.type.tree import Tree
from typing import cast


class Database:

    @staticmethod
    def _read_data(hash: Hash) -> DataReader:
        path = Database._database_path(hash.database_path())

        compressed = FileManager.read_file(path)
        decompressed = gzip.decompress(compressed)

        return DataReader(decompressed)

    @staticmethod
    def _write_data(data: bytes):
        hash = Hash.from_contents(data)
        path = Database._database_path(hash.database_path())

        compressed = gzip.compress(data)

        FileManager.write_file(path, compressed)

    @staticmethod
    def read_object(hash: Hash) -> Object:
        data_reader = Database._read_data(hash)

        return Object.from_reader(data_reader)

    @staticmethod
    def write_object(object: Object):
        Database._write_data(object.get_data())

    @staticmethod
    def _database_path(path: str) -> str:
        return f"objects/{path}"

    @staticmethod
    def complete_hash(partial_hash: str) -> Hash:
        subset = partial_hash[:2]

        candidates = Database.get_subset(subset)
        matches = [h for h in candidates if str(h).startswith(partial_hash)]

        match len(matches):
            case 0: raise ValueError(f"no hashes matching partial: {partial_hash}")
            case 1: return matches[0]
            case _: raise ValueError(f"Abiguous hash prefix: {partial_hash}, matches: {[str(h) for h in matches]}")

    @staticmethod
    def get_subset(subset: str) -> list[Hash]:
        output = []

        subset_path = Database._database_path(subset)
        for path in FileManager.listdir(subset_path):
            path = os.path.join(subset_path, path)
            output.append(Hash.from_path(path))

        return output

    @staticmethod
    def _create_blob_reference(path: str) -> ObjectReference:
        contents = FileManager.bytes_to_str(FileManager.read_file(path, True))
        blob = Blob(contents)
        name = os.path.basename(path)

        return ObjectReference.from_object(blob, name)

    @staticmethod
    def _create_tree_reference(path: str) -> ObjectReference:
        if not FileManager.is_dir(path):
            return Database._create_blob_reference(path)

        tree = Tree()
        name = os.path.basename(path)

        for dir in FileManager.listdir(path, True):
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
            FileManager.write_file(path, FileManager.str_to_bytes(object.contents), True)
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
