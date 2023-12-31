from backend import db


class UserEnrollEventModel(db.Model):
    __tablename__ = "user_enroll_event_table"
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user_table.user_id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey(
        'event_info_table.event_id'), primary_key=True)

    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id

    def __eq__(self, other):
        return (
            self.user_id == other.user_id and
            self.event_id == other.event_id
        )
