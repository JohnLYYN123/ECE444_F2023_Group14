from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user, logout_user
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import (DateTimeField, PasswordField, StringField, BooleanField,
                     ValidationError, SubmitField)
from wtforms.validators import InputRequired, Length, EqualTo, Optional, Email, Regexp
# from backend import login_manager
user = Blueprint("user", __name__, url_prefix="/user")


class register_form(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(1, 20, message="Please provide a valid name"),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message='Username must contain only letters, numbers, or underscores.'
            )
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
        validators=[InputRequired(), Email(), Length(max=50)])
    uoft_student_id = StringField(validators=[Optional()])
    first_name = StringField(validators=[Optional()])
    last_name = StringField(validators=[Optional()])
    department = StringField(validators=[Optional()])
    enrolled_time = DateTimeField(validators=[Optional()])
    submit = SubmitField('Sign Up')

    def validate_email(self, uoft_email):
        from models.user import User  # noqa
        if User.query.filter_by(uoft_email=uoft_email.data).first():
            raise ValidationError("Email already registered!")

    def validate_uname(self, uname):
        from models.user import User  # noqa
        if User.query.filter_by(username=uname.data).first():
            raise ValidationError("Username already taken!")


class login_form(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(1, 20, message="Please provide a valid name"),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message='Username must contain only letters, numbers, or underscores.'
            )
        ]
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=1, max=20)])
    # if the username does not exist
    submit = SubmitField('Login')

    def validate_uname(self, uname):
        from models.user import User  # noqa
        if not User.query.filter_by(username=uname.data).first():
            raise ValidationError("Username already taken!")

# @login_manager.user_loader
# def load_user(user_id):
#     # This callback is used to reload the user object
#     # from the user ID stored in the session
#     from models.user import User
#     return User.query.get(int(user_id))


@user.route("register", methods=['POST', 'GET'])
# @login_required
def register():
    form = register_form()
    if form.validate_on_submit() and request.method == 'POST':
        try:
            from models.user import User  # noqa
            user = User.query.filter_by(username=form.username)
            if user is None:
                username = form.username.data
                uoft_email = form.uoft_email.data
                pwd = form.password.data
                from backend import bcrypt  # noqa
                newuser = User(
                    username=username,
                    uoft_email=uoft_email,
                    password=bcrypt.generate_password_hash(pwd),
                )
                from backend import db  # noqa
                db.session.add(newuser)
                db.session.commit()
                flash(f"Account Succesfully created", "success")
                return redirect(url_for("login"))

        except Exception as e:
            flash(e, "danger")


@user.route("/login", methods=['POST'])
def login():
    from backend import db
    from models.user_model import UserModel
    if current_user.is_authenticated:
        return redirect(url_for('user/register'))
    form = login_form()


@user.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!  Thanks For Stopping By...")
    return redirect(url_for('login'))

    # if form.validate_on_submit():


#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({'message': 'One of the entries is empty'}), 401
#     else:
#         return jsonify({'message': 'Login successful'}), 200
