from backend import app, db
from models import event_info, event_filter, user

with app.app_context():
    # create the database and the db table

    # please use the drop_all API cautious, it will drop every table created
    # db.drop_all()
    db.create_all()
    # commit the changes
    db.session.commit()
