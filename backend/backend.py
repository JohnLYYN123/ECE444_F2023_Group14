# from app import create_app
from pathlib import Path
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


basedir = Path(__file__).resolve().parent
app = Flask(__name__)


# set db paths
DATABASE = "uevent.db"
SQLALCHEMY_DATABASE_URI_1 = "sqlite:///" + str(Path(basedir).joinpath(DATABASE))  # noqa
SQLALCHEMY_TRACK_MODIFICATIONS_1 = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS_1


# initialize DB
db = SQLAlchemy(app)
# initialize route path
user = Blueprint("user", "user_authentication_system.py", url_prefix="/user")
main_sys = Blueprint("main_sys", "main_system.py", url_prefix="/main_sys")
detail = Blueprint("detail", "detailed_system.py", url_prefix="/detail")
app.register_blueprint(user)
app.register_blueprint(main_sys)
app.register_blueprint(detail)
# cors add
CORS(app, resources={r"/user/*": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/main_sys/*": {"origins": "http://localhost:3000"}})


if __name__ == "__main__":
    app.run(debug=True)
