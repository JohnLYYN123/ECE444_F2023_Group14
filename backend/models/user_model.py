from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from backend import db


class UserModel(db.Model):

    __tablename__ = 'user_table'
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # must have username, passoword and uoft_email
    username = db.Column(db.String(20), unique=True, nullable=False)
    uoft_email = db.Column(db.String(50), unique=True, nullable=False)
    # the orginaztion table is not ready rn, need to add
    # supplementary information needed
    uoft_student_id = db.Column(db.String(20))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    department = db.Column(db.String(50))
    enrolled_time = db.Column(db.String(20))
    password_hash = db.Column(db.String(128), nullable=False)
    # columns used for post events, check hosts
    organizational_role = db.Column(db.Boolean, default=False)

    def get_id(self):
        """Return the user id"""
        return self.user_id

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def is_host(self):
        """Return True if the user is a host."""
        return self.organizational_role

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @property
    def formatted_enrolled_time(self):
        if self.enrolled_time:
            enrolled_time_datetime = datetime.strptime(
                self.enrolled_time, "%m/%Y")
            return enrolled_time_datetime.strftime("%m/%Y")
        else:
            return None

    @password.setter
    def password(self, password):
        from backend import bcrypt  # noqa
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        from backend import bcrypt  # noqa
        return bcrypt.check_password_hash(self.password_hash, password)

    def __init__(self, username, uoft_email, password_hash, uoft_student_id, first_name, last_name, department, enrolled_time, organizational_role):
        self.username = username
        self.uoft_email = uoft_email
        self.password_hash = password_hash
        self.uoft_student_id = uoft_student_id
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.enrolled_time = enrolled_time
        self.organizational_role = organizational_role
