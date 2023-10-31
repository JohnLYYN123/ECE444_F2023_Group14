from pathlib import Path

basedir = Path(__file__).resolve().parent

DATABASE_1 = "event_filter.db"
SQLALCHEMY_DATABASE_URI_1 = f"sqlite:///{Path(basedir).joinpath(DATABASE_1)}"
SQLALCHEMY_TRACK_MODIFICATIONS_1 = False


if __name__ == '__main__':
    print(basedir)
    print(Path(basedir).joinpath(DATABASE_1))


