from datetime import datetime
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
# from backend import db


db1 = SQLAlchemy()
db2= SQLAlchemy()
class EventFilerDB(db1.Model):
    __tablename__ = "event_filter_db"
    event_id = db1.Column(db1.Integer, primary_key=True)
    filter = db1.Column(db1.String(256), primary_key=True)
    create_time = db1.Column(db1.DateTime, default=datetime.utcnow())
    update_time = db1.Column(db1.DateTime, onupdate=datetime.utcnow())

    filter_check = CheckConstraint(
        "filter IN ('sport', 'art', 'travel', 'cooking')", name="filter_check_constraint")

    def __init__(self, event_id, filter_name):
        self.event_id = event_id
        self.filter = filter_name
