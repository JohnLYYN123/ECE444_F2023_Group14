from backend import app, db
from mock_data import event_info_mocking
"""
DO NOT REMOVE THE FOLLOWING LINES, AND PLEASE EXECUTE WITH CAUTION
"""
from models import user_model, event_info_model
from models import review_rating_model
from models import user_enroll_event_model, user_organize_club_model
from models import host_event_model
from models.event_info_model import ClubInfoModel, EventInfoModel

with app.app_context():
    # create the database and the db table

    # please use the drop_all API cautious, it will drop every table created
    db.drop_all()
    db.create_all()

    # commit the changes
    db.session.commit()
    event_info_mocking(db)
