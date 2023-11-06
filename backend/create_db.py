from backend import app, db
from mock_data import event_info_mocking
"""
DO NOT REMOVE THE FOLLOWING LINES, AND PLEASE EXECUTE WITH CAUTION
"""
from models import user, event_info_model
from models import club_info_model, event_filter_model, review_rating_model
from models import user_enroll_event_model, user_organize_club_model

with app.app_context():
    # create the database and the db table

    # please use the drop_all API cautious, it will drop every table created
    # db.drop_all()
    db.create_all()

    # commit the changes
    db.session.commit()
    event_info_mocking(db)

