# from app import create_app
from routes.main_system import main_sys
from routes.detailed_system import detail
from routes.user_authentication_system import user
from pathlib import Path
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# print("!23123")
# initialize route path
app.register_blueprint(user)
app.register_blueprint(main_sys)
app.register_blueprint(detail)

# cors add
CORS(app, resources={r"/user/*": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/main_sys/*": {"origins": "http://localhost:3000"}})

basedir = Path(__file__).resolve().parent
# set db paths
DATABASE = "uevent.db"
SQLALCHEMY_DATABASE_URI_1 = "sqlite:///" + str(Path(basedir).joinpath(DATABASE))  # noqa
SQLALCHEMY_TRACK_MODIFICATIONS_1 = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS_1

# initialize DB
db = SQLAlchemy(app)
