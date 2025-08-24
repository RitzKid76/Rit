import os

from object.database import Database
from object.hash import Hash


def populate_database_for_testing():
    for dirpath, _, files in os.walk(os.getcwd()):
        if "database" in dirpath or "__pycache__" in dirpath or ".git" in dirpath:
            continue

        for file in files:
            full_path = os.path.join(dirpath, file)
            blob_reference = Database._create_blob_reference(full_path)
            Database.write_object(blob_reference.get_object())


def read_database_for_testing():
    for dirpath, _, files in os.walk(os.getcwd()):
        if "database" not in dirpath:
            continue

        for file in files:
            path = os.path.join(dirpath, file)
            print(Database.read_object(Hash.from_path(path)).get_data())


def main():
    # populate_database_for_testing()
    # read_database_for_testing()

    Database.store("test")
    # Database.load(Hash.from_partial("810"))


if __name__ == "__main__":
    main()
