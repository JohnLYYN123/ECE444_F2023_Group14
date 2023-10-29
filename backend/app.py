from flask import Flask

from routes.user_authentication_system import user

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user)
    return app
