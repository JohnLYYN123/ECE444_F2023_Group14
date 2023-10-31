from datetime import datetime
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from backend import db


class EventFilerDB(db.Model):
    # __tablename__ = "event_filter_db"
    event_id = db.Column(db.Integer, primary_key=True)
    filter = db.Column(db.String(256), primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    update_time = db.Column(db.DateTime, onupdate=datetime.utcnow())

    filter_check = CheckConstraint(
        "filter IN ('sport', 'art', 'travel', 'cooking')", name="filter_check_constraint")

    def __init__(self, event_id, filter_name):
        self.event_id = event_id
        self.filter = filter_name
