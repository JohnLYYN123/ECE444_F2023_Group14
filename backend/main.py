# from app import create_app
from routes.main_system import main_sys
from routes.detailed_system import detail
from routes.user_authentication_system import user
from pathlib import Path
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from backend import app, db

if __name__ == "__main__":
    app.run(debug=True)
