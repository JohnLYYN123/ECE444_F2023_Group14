from sqlalchemy import text
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user
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
        from models.user_model import UserModel  # noqa
        if UserModel.query.filter_by(uoft_email=uoft_email.data).first():
            raise ValidationError("Email already registered!")

    def validate_uname(self, uname):
        from models.user_model import UserModel  # noqa
        if UserModel.query.filter_by(username=uname.data).first():
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
        from models.user_model import UserModel  # noqa
        if not UserModel.query.filter_by(username=uname.data).first():
            raise ValidationError("Username already taken!")


@user.route('/view')
def view_user():
    sql = text("select * from user_table;")
    from models.user_model import UserModel  # noqa
    res = UserModel.query.from_statement(sql).all()
    result = []
    for i in res:
        event_dict = {"user_id": i.user_id,
                      "user_name": i.username,
                      "uoft_email": i.uoft_email}
        result.append(event_dict)
    return jsonify({"code": 200, "msg": "OK", "data": result}), 200


@user.route("register", methods=['POST', 'GET'])
def register():
    uname = None
    form = register_form()
    session.pop('_id', None)
    if form.validate_on_submit():
        try:
            from models.user_model import UserModel  # noqa
            user = UserModel.query.filter_by(
                username=form.username.data).first()
            # print(f"Form username: {form.username.data}")
            # print(f"Usernames from the database: {
            #       [user.username for user in UserModel.query.all()]}")
            if user is None:
                from backend import bcrypt  # noqa
                username_on_form = form.username.data
                email_on_form = form.uoft_email.data
                password = bcrypt.generate_password_hash(
                    form.password.data)
                student_id_on_form = form.uoft_student_id.data
                frist_name_on_form = form.first_name.data
                last_name_on_form = form.last_name.data
                department_on_form = form.department.data
                enrolled_time_on_form = form.enrolled_time.data
                newuser = UserModel(
                    username=username_on_form,
                    uoft_email=email_on_form,
                    password_hash=password,
                    uoft_student_id=student_id_on_form,
                    first_name=frist_name_on_form,
                    last_name=last_name_on_form,
                    department=department_on_form,
                    enrolled_time=enrolled_time_on_form,
                    authenticated=True,
                )
                from backend import db  # noqa
                db.session.add(newuser)
                db.session.commit()
                uname = form.username.data
                form.username.data = ''
                form.uoft_email.data = ''
                form.password.data = ''
                form.uoft_student_id.data = ''
                form.first_name.data = ''
                form.last_name.data = ''
                form.department.data = ''
                form.enrolled_time.data = ''
                # Store user_id in the session
                session['_id'] = newuser.user_id
                flash(f"Account Succesfully created", "success")
                return jsonify({"code": 200, "msg": "Registration successfully."}), 200
            else:
                flash(f"The user name has been created before")
                return jsonify({"code": 400, "msg": "The username has been used."}), 400
        except Exception as e:
            flash(e, f"User registration has problems")
    return render_template("add_user.html",
                           form=form,
                           name=uname,)
    # return redirect(url_for("login"))


@user.route("/login", methods=['POST', 'GET'])
def login():
    form = login_form()
    session.pop('id', None)
    if form.validate_on_submit():
        # Check the hash
        username = form.username.data
        password = form.password.data
        from models.user_model import UserModel  # noqa
        user = UserModel.query.filter_by(username=username).first()
        if user and user.is_authenticated:
            from backend import bcrypt  # noqa
            if bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Succesfull!!")
                session['_id'] = user.user_id
                return jsonify({"code": 200, "msg": "Login Succesfull."}), 200
                # return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try Again!")
                return jsonify({"code": 400, "msg": "Wrong passowrd"}), 400
    return render_template('login.html', form=form)
    # return redirect(url_for("main_page"))


# @user.route('/logout', methods=['GET', 'POST'])
# @login_required
# def logout():
#     logout_user()
#     flash("You Have Been Logged Out!  Thanks For Stopping By...")
#     return jsonify({"code": 200, "msg": "Log out Succesfully."}), 200
#     return redirect(url_for('user.login'))

#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({'message': 'One of the entries is empty'}), 401
#     else:
#         return jsonify({'message': 'Login successful'}), 200
