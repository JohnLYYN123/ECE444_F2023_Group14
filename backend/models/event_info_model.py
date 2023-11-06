from datetime import datetime
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from backend import db
# from .event_filter import EventFilerDB # noqa


class EventInfoModel(db.Model):
    __tablename__ = "event_info_table"
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_name = db.Column(db.String(256), nullable=False)
    event_time = db.Column(db.DateTime, nullable=False)
    number_rater = db.Column(db.Integer)
    average_rating = db.Column(db.Double)
    event_description = db.Column(db.Text, nullable=False)
    # todo: add proper pictures
    address = db.Column(db.String)
    charge = db.Column(db.Double)
    shared_title = db.Column(db.String)
    shared_image = db.Column(db.String)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    update_time = db.Column(db.DateTime, onupdate=datetime.utcnow())

    club_id = db.Column(db.Integer, db.ForeignKey(
        'club_info_table.club_id'), default=None)

    # eid = db.relationship('EventInfoDB', backref='EventFilerDB')

    @property
    def event_time(self):
        return self._event_time

    @event_time.setter
    def event_time(self, value):
        if value is None:
            self._event_time = None
        elif isinstance(value, str):
            self._event_time = datetime.strptime(value, '%Y-%m-%dT%H:%M')
        elif isinstance(value, datetime):
            self._event_time = value
        else:
            raise ValueError(
                "Invalid input format for event_time. Expecting string or datetime object.")

    def __init__(
        self,
        event_name,
        event_time,
        event_description,
        address=None,
        charge=None,
        shared_title=None,
        shared_image=None,
        club_id=None,
        number_rater=0,  # Default value for number_rater
        average_rating=0.0  # Default value for average_rating
    ):
        self.event_name = event_name
        self.event_time = event_time
        self.number_rater = number_rater
        self.average_rating = average_rating
        self.event_description = event_description
        self.address = address
        try:
            self.charge = float(charge) if charge else 0.0
        except (ValueError, TypeError):
            self.charge = 0.0
            self.shared_title = shared_title
        self.shared_image = shared_image
        self.club_id = club_id


class ClubInfoModel(db.Model):
    __tablename__ = 'club_info_table'
    club_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_name = db.Column(db.String(256), unique=True, nullable=False)
    host_name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    event = db.relationship('EventInfoModel', backref='club', lazy=True)

    def __init__(self, club_name=None, host_name=None, description=None):
        self.club_name = club_name
        self.host_name = host_name
        self.description = description


def club_info_model_print(club_info_instance: ClubInfoModel):
    print('club_id: ', club_info_instance.club_id, 'club_name: ', club_info_instance.club_name, '; host_name: ',
          club_info_instance.host_name, '; description: ', club_info_instance.description)
