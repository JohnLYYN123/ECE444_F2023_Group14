from re import RegexFlag
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import (DateTimeField, EmailField, PasswordField, StringField, BooleanField,
                     ValidationError, SubmitField)
from wtforms.validators import InputRequired, Length, DataRequired, EqualTo, Optional
from models.user import User


class register_form(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(1, 20, message="Please provide a valid name"),
            RegexFlag(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, numbers, dots or underscores",
            ),
        ]
    )
    password = PasswordField(validators=[InputRequired(), Length(1, 20)])
    repeat_password = PasswordField(
        validators=[
            InputRequired(),
            Length(1, 20),
            EqualTo("password", message="Passwords must match!"),
        ]
    )
    # can do later, if we want to add uoft email suffix
    uoft_email = StringField(
        validators=[InputRequired(), EmailField(), Length(max=50)])
    uoft_student_id = StringField(validators=[Optional()])
    first_name = StringField(validators=[Optional()])
    last_name = StringField(validators=[Optional()])
    department = StringField(validators=[Optional()])
    enrolled_time = DateTimeField(validators=[Optional()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        if User.query.filter_by(uoft_email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_uname(self, uname):
        if User.query.filter_by(username=uname.data).first():
            raise ValidationError("Username already taken!")


class login_form(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(1, 20, message="Please provide a valid name"),
            RegexFlag(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, numbers, dots or underscores",
            ),
        ]
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=1, max=20)])
    # if the username does not exist
    submit = SubmitField('Login')

    def validate_uname(self, uname):
        if not User.query.filter_by(username=uname.data).first():
            raise ValidationError("Username already taken!")
