from app import create_app
from flask_cors import CORS
from routes.Database import config

app = create_app()
# app = Flask(__name__)
# set db paths
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI_1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS_1

# initialize DB
from routes.Database.Event_DB import t_event_filter_db
t_event_filter_db.init_app(app)

with app.app_context():
    # create the database and the db table
    t_event_filter_db.create_all()

    # commit the changes
    t_event_filter_db.session.commit()

CORS(app, resources={r"/user/*": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/main_sys/*": {"origins": "http://localhost:3000"}})
if __name__ == "__main__":
    app.run(debug=True)
