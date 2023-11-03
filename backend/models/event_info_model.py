from datetime import datetime
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from backend import db
#from .event_filter import EventFilerDB # noqa

class EventInfoModel(db.Model):
    __tablename__ = "event_info_table"
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_name = db.Column(db.String(256))
    event_time = db.Column(db.DateTime)
    number_rater = db.Column(db.Integer)
    average_rating = db.Column(db.Double)
    event_description = db.Column(db.String(256))

    # todo: add proper pictures


    # todo: fixed proper address
    position_addre = db.Column(db.String)
    address = db.Column(db.String)

    charge = db.Column(db.Double)


    shared_title = db.Column(db.String)
    shared_image = db.Column(db.String)

    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    update_time = db.Column(db.DateTime, onupdate=datetime.utcnow())

    club_id = db.Column(db.Integer, db.ForeignKey('club_info_table.club_id'))

    # eid = db.relationship('EventInfoDB', backref='EventFilerDB')


    def __init__(
        self,
        event_name,
        event_time,
        number_rater,
        average_rating,
        event_description,
    ):
        self.event_name = event_name
        self.event_description = event_time
        self.number_rater = number_rater
        self.average_rating = average_rating
        self.event_description = event_description


