import os


class FileManager:

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
    def is_dir(path: str) -> bool:
        return os.path.isdir(path)

    @staticmethod
    def read_file(path: str, external: bool = False) -> bytes:
        path = FileManager._wrap_internal(path, external)

        with open(path, "rb") as f:
            return f.read()

    @staticmethod
    def write_file(path: str, contents: str | bytes, external: bool = False):
        path = FileManager._wrap_internal(path, external)

        FileManager._create_folder(path)

        if isinstance(contents, str):
            contents = FileManager.str_to_bytes(contents)

        with open(path, "wb") as f:
            f.write(contents)

    @staticmethod
    def listdir(path: str, external: bool = False) -> list[str]:
        path = FileManager._wrap_internal(path, external)

        return os.listdir(path)

    @staticmethod
    def _wrap_internal(path: str, external: bool) -> str:
        return path if external else f".rit/{path}"
