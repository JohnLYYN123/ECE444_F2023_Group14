from app import create_app
from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/user/*": {"origins": "http://localhost:3000"}})

if __name__ == "__main__":
    app.run(debug=True)
