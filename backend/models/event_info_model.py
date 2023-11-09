from datetime import datetime
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from backend import db
# from .event_filter import EventFilerDB # noqa


class EventInfoModel(db.Model):
    __tablename__ = "event_info_table"
    __table_args__ = {'extend_existing': True}

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
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    update_time = db.Column(db.DateTime, onupdate=datetime.utcnow())

    club_id = db.Column(db.Integer, db.ForeignKey(
        'club_info_table.club_id'), default=None)

    # eid = db.relationship('EventInfoDB', backref='EventFilerDB')
    def __init__(
        self,
        event_name,
        event_time,
        event_description,
        address=None,
        charge=None,
        shared_title=None,
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
        self.club_id = club_id

    def __eq__(self, other):
        if isinstance(self.event_time, str):
            self.event_time = datetime.strptime(
                self.event_time, '%m/%d/%Y %H:%M')
        if isinstance(other.event_time, str):
            other.event_time = datetime.strptime(
                other.event_time, '%m/%d/%Y %H:%M')
        return (
            self.event_name == other.event_name and
            self.event_time.strftime('%m/%d/%Y %H:%M') == other.event_time.strftime('%m/%d/%Y %H:%M') and
            self.event_description == other.event_description and
            self.address == other.address and
            self.charge == other.charge and
            self.shared_title == other.shared_title and
            self.club_id == other.club_id
        )


class ClubInfoModel(db.Model):
    __tablename__ = 'club_info_table'
    __table_args__ = {'extend_existing': True}

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
