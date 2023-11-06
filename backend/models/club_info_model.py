from backend import db

class ClubInfoModel(db.Model):
    __tablename__ = 'club_info_table'
    club_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_name = db.Column(db.String(256), unique=True, nullable=False)
    host_name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)

    def __init__(self, club_dict):
        self.club_name = club_dict['club_name']
        self.host_name = club_dict['host_name']
        self.description = club_dict['description']


def club_info_model_print(club_info_instance: ClubInfoModel):
    print('club_id: ', club_info_instance.club_id, 'club_name: ', club_info_instance.club_name, '; host_name: ',
          club_info_instance.host_name, '; description: ', club_info_instance.description)
