# from app import create_app
from routes.main_system import main_sys
from routes.detailed_system import detail
from routes.user_authentication_system import user
from pathlib import Path
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from backend import app, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    # This callback is used to reload the user object
    # from the user ID stored in the session
    from models.user_model import UserModel
    return UserModel.query.get(int(user_id))


if __name__ == "__main__":
    app.run(debug=True)
