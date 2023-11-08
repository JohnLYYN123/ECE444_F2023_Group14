from backend import app, db
from mock_data import event_info_mocking, filter_info_mocking, club_info_mocking

"""
DO NOT REMOVE THE FOLLOWING LINES, AND PLEASE EXECUTE WITH CAUTION
"""
from backend.models.review_rating_model import ReviewRatingModel
from backend.models.user_organize_club_model import UserOrganizeClubModel
from backend.models.host_event_model import HostEventModel
from backend.models.user_model import UserModel
from backend.models.event_info_model import ClubInfoModel, EventInfoModel
from backend.models.user_enroll_event_model import UserEnrollEventModel

with app.app_context():
    # create the database and the db table

    # please use the drop_all API cautious, it will drop every table created
    db.drop_all()
    db.create_all()

    # commit the changes
    db.session.commit()
    event_info_mocking(db)
    filter_info_mocking(db)
    club_info_mocking(db)


