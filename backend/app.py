from flask import Flask
from routes.user_authentication_system import user
from routes.main_system import main_sys

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user)
    app.register_blueprint(main_sys)
    return app
