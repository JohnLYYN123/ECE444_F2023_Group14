from datetime import datetime
from sqlite3 import IntegrityError
from sqlalchemy import text
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import (DateTimeField, PasswordField, StringField, BooleanField,
                     ValidationError, SubmitField)
from wtforms.validators import InputRequired, Length, EqualTo, Optional, Email, Regexp
import json

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
    enrolled_time = StringField(validators=[
        Optional(),
        Regexp(r'^\d{2}/\d{4}$', message='Invalid format. Please use MM/YYYY.')
    ])
    organizational_role = BooleanField(validators=[Optional()])
    submit = SubmitField('Sign Up')


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


@user.route('/view')
def view_user():
    sql = text("select * from user_table;")
    from models.user_model import UserModel  # noqa
    res = UserModel.query.from_statement(sql).all()
    result = []
    for i in res:
        event_dict = {"user_id": i.user_id,
                      "user_name": i.username,
                      "uoft_email": i.uoft_email,
                      "organizational_role": i.organizational_role,
                      "enrolled_time": i.enrolled_time,
                      }
        result.append(event_dict)
    return jsonify({"code": 200, "msg": "OK", "data": result}), 200


@user.errorhandler(Exception)
def handle_error(error):
    status_code = 500  # Default status code for Internal Server Error
    message = str(error)

    # Check if the exception has a status_code attribute
    if hasattr(error, 'status_code'):
        status_code = error.status_code

    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }

    flash(f"Error: {message}", 'error')  # Flash the error message as a string
    return response, status_code


@user.route("register", methods=['POST', 'GET'])
def register():
    uname = None
    form = register_form()
    #  and request.method == 'POST'
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
                enrolled_time_data = form.enrolled_time.data
                organizational_role_on_form = form.organizational_role.data
                newuser = UserModel(
                    username=username_on_form,
                    uoft_email=email_on_form,
                    password_hash=password,
                    uoft_student_id=student_id_on_form,
                    first_name=frist_name_on_form,
                    last_name=last_name_on_form,
                    department=department_on_form,
                    enrolled_time=enrolled_time_data,
                    authenticated=True,
                    organizational_role=organizational_role_on_form,
                )
                formatted_enrolled_time = newuser.formatted_enrolled_time
                newuser.enrolled_time = formatted_enrolled_time
                from backend import db  # noqa
                db.session.add(newuser)
                db.session.commit()
                # clear form data
                form.username.data = ''
                form.uoft_email.data = ''
                form.password.data = ''
                form.uoft_student_id.data = ''
                form.first_name.data = ''
                form.last_name.data = ''
                form.department.data = ''
                form.enrolled_time.data = ''
                flash(f"Account Succesfully created", "success")
                return jsonify({"code": 200, "msg": "Registration successfully."}), 200
                # return redirect(url_for("main_page"))
        except Exception as e:
            response, status_code = handle_error(e)
            flash(response['error']['message'], 'error')
            return jsonify(response), status_code
    else:
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append({
                    'field': field,
                    'message': error
                })

        response = {
            'success': False,
            'error': {
                'type': 'ValidationError',  # Custom error type for validation errors
                'messages': error_messages  # List of error messages with corresponding fields
            }
        }

        # Flash individual error messages
        for error in error_messages:
            flash(f"Field '{error['field']}': {error['message']}", 'error')

    # elif request.method == 'GET':
    #     return jsonify({"code": 405, "msg": "Method not allowed."}), 405
    return render_template("add_user.html",
                           form=form,
                           name=uname,)


@user.route("/login", methods=['POST', 'GET'])
def login():
    form = login_form()
    #  and request.method == 'POST'
    if form.validate_on_submit():
        try:
            # Check the hash
            username = form.username.data
            password = form.password.data
            from models.user_model import UserModel  # noqa
            user = UserModel.query.filter_by(username=username).first()
            if user and user.is_authenticated:
                from backend import bcrypt  # noqa
                if bcrypt.check_password_hash(user.password_hash, password):
                    login_user(user)
                    flash("Login Succesfull!!")
                    return jsonify({"code": 200, "msg": "Login Succesfull."}), 200
                    # return redirect(url_for('mainpage'))
                else:
                    flash("Wrong Password - Try Again!")
                    return redirect(url_for('user.login'))
        except Exception as e:
            response, status_code = handle_error(e)
            flash(response['error']['message'], 'error')
            return jsonify(response), status_code
    # elif request.method == 'GET':
    #     return jsonify({"code": 405, "msg": "Method not allowed."}), 405
    else:
        return render_template('login.html', form=form)


@user.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!  Thanks For Stopping By...")
    return jsonify({"code": 200, "msg": "Log out Succesfully."}), 200
