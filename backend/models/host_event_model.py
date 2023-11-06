from backend import db


class HostEventModel(db.Model):
    __tablename__ = "host_event_table"
    host_id = db.Column(db.Integer, db.ForeignKey(
        'user_table.user_id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey(
        'event_info_table.event_id'), primary_key=True)

    def __init__(self, host_id, event_id):
        self.host_id = host_id
        self.event_id = event_id
