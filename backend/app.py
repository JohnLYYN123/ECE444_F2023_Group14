from flask import Flask

from routes.user_authentication_system import user
from Controllers.SearchController import search

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user)
    app.register_blueprint(search)
    return app
