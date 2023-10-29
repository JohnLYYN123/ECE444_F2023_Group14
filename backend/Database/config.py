from pathlib import Path

basedir = Path(__file__).resolve().parent

DATABASE = "Event.db"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{Path(basedir).joinpath(DATABASE)}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
