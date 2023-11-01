from backend import db, app
from models import Event_model
with app.app_context():
    # create the database and the db table
    # db.drop_all()
    db.create_all()
    # commit the changes
    db.session.commit()
