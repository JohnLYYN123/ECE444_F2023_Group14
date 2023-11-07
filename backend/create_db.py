from backend import app, db
from mock_data import event_info_mocking, filter_info_mocking

"""
DO NOT REMOVE THE FOLLOWING LINES, AND PLEASE EXECUTE WITH CAUTION
"""
from models import event_info_model
from models import review_rating_model
from models import user_organize_club_model
from models import host_event_model
from models.user_model import UserModel
from models.event_info_model import ClubInfoModel, EventInfoModel
from models.user_enroll_event_model import UserEnrollEventModel

with app.app_context():
    # create the database and the db table

    # please use the drop_all API cautious, it will drop every table created
    db.drop_all()
    db.create_all()

    # commit the changes
    db.session.commit()
    event_info_mocking(db)
    filter_info_mocking(db)
