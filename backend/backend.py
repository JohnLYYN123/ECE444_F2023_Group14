from app import create_app
from flask_cors import CORS
from Database import config
from flask_sqlalchemy import SQLAlchemy

app = create_app()
#app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

CORS(app, resources={r"/user/*": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/main_sys/*": {"origins": "http://localhost:3000"}})
if __name__ == "__main__":
    app.run()
