from datetime import datetime
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from backend import db
#from .event_filter import EventFilerDB # noqa

class EventInfoDB(db.Model):
    __tablename__ = "event_info"
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(256))
    event_desc = db.Column(db.String(256))
    organizer = db.Column(db.String(256))
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    update_time = db.Column(db.DateTime, onupdate=datetime.utcnow())

    # eid = db.relationship('EventInfoDB', backref='EventFilerDB')


    def __init__(self, event_id, event_name, event_desc, organizer):
        self.event_id = event_id
        self.event_name = event_name
        self.event_desc = event_desc
        self.organizer = organizer

