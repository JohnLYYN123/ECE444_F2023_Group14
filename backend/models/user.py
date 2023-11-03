from flask_sqlalchemy import SQLAlchemy
from backend import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # must have username, passoword and uoft_email
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    uoft_email = db.Column(db.String(50), unique=True, nullable=False)
    # the orginaztion table is not ready rn, need to add
    # supplementary information needed
    # store student_id as a string, as the passed in data from frontend would be string
    uoft_student_id = db.Column(db.String(20))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    department = db.Column(db.String(50))
    enrolled_time = db.Column(db.DateTime)  # rename of school_year column
    # authorziation check used column
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the user id"""
        return self.user_id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    @property
    def formatted_enrolled_time(self):
        return self.enrolled_time.strftime("%m/%Y")

    def __init__(self, username=None, password=None, uoft_email=None,
                 uoft_student_id=None, first_name=None, last_name=None,
                 department=None, enrolled_year=None, authenticated=False):
        self.username = username
        self.password = password
        self.uoft_email = uoft_email
        self.uoft_student_id = uoft_student_id
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.enrolled_year = enrolled_year
        self.authenticated = authenticated
