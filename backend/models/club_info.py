from backend import db

class ClubInfoDB(db.Model):
    __tablename__ = "club_info"
    club_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_name = db.Column(db.String(256), nullable=False)
    host_name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)

    def __init__(self, club_dict):
        self.club_id = club_dict["club_id"]
        self.club_name = club_dict["club_name"]
        self.host_name = club_dict["host_name"]
        self.description = club_dict["description"]