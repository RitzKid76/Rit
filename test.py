import os

from object.database import Database
from object.hash import Hash


def populate_database_for_testing():
    for dirpath, _, files in os.walk(os.getcwd()):
        if "database" in dirpath or "__pycache__" in dirpath:
            continue

        for file in files:
            full_path = os.path.join(dirpath, file)
            contents = Database._read_file(full_path)
            Database._write_data(contents)


def main():
    populate_database_for_testing()

    hash = Hash.from_partial("5f09")
    print(Database.read_object(hash))


if __name__ == "__main__":
    main()
