# from app import create_app
from backend.routes.main_system import main_sys
from backend.routes.detailed_system import detail
from backend.routes.user_authentication_system import user
from backend.routes.enrollment_cart_system import enroll
from pathlib import Path
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# print("!23123")
# initialize route path
app.register_blueprint(user)
app.register_blueprint(main_sys)
app.register_blueprint(detail)
app.register_blueprint(enroll)

CORS(app)

# cors add
CORS(app, resources={r"/user/*": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/detail/*": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/main_sys/*": {"origins": "http://localhost:3000"}})
CORS(app, resources={
     r"/detail/register/*": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/enroll/*": {"origins": "http://localhost:3000"}})


basedir = Path(__file__).resolve().parent
# set db paths
DATABASE = "uevent.db"
SQLALCHEMY_DATABASE_URI_1 = "sqlite:///" + str(Path(basedir).joinpath(DATABASE))  # noqa
SQLALCHEMY_TRACK_MODIFICATIONS_1 = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS_1
app.config['SECRET_KEY'] = 'any secret string'
app.config['SESSION_TYPE'] = 'memcached'


# initialize DB
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
