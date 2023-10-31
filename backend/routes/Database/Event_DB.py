from datetime import datetime
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

t_event_filter_db = SQLAlchemy()
class EventFilerDB(t_event_filter_db.Model):
    __tablename__ = "event_filter_db"
    event_id = t_event_filter_db.Column(t_event_filter_db.Integer, primary_key=True)
    filter = t_event_filter_db.Column(t_event_filter_db.String(256), primary_key=True)
    create_time = t_event_filter_db.Column(t_event_filter_db.DateTime, default=datetime.utcnow())
    update_time = t_event_filter_db.Column(t_event_filter_db.DateTime, onupdate=datetime.utcnow())

    filter_check = CheckConstraint("filter IN ('sport', 'art', 'travel', 'cooking')", name="filter_check_constraint")

    def __init__(self, event_id, filter_name):
        self.event_id = event_id
        self.filter = filter_name



