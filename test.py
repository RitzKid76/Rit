from object.database import Database
from object.hash import Hash


def main():
    # Database.store("test")
    Database.load(Hash.from_partial("810"))


if __name__ == "__main__":
    main()
