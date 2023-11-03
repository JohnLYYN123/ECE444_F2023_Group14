from datetime import datetime
from pprint import pprint
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from backend import db
#from .event_info import EventInfoDB # noqa



class EventFilerDB(db.Model):
    __tablename__ = "event_filter"
    event_id = db.Column(db.Integer, db.ForeignKey('event_info.event_id', ondelete="CASCADE"), primary_key=True)
    filter = db.Column(db.String(256),
                       CheckConstraint("filter IN ('sport', 'art', 'travel', 'cooking')", name="filter_check_constraint"),
                       primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    update_time = db.Column(db.DateTime, onupdate=datetime.utcnow())

    #filter_ref = db.relationship('EventInfoDB', primaryjoin="EventFilerDB.event_id==EventInfoDB.event_id")


    def __init__(self, event_id, filter_name):
        self.event_id = event_id
        self.filter = filter_name



