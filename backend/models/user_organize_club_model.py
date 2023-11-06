from backend import db


class UserOrganizeClubModel(db.Model):
    __tablename__ = "user_organize_club_table"
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user_table.user_id"), primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey(
        "club_info_table.club_id"), primary_key=True)

    def __init__(self, user_id, club_id):
        self.user_id = user_id
        self.club_id = club_id

    def get_user_id(self):
        return self.user_id

    def get_club_id(self):
        return self.club_id
