from datetime import datetime
from sqlite3 import IntegrityError
from sqlalchemy import text
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user, current_user

user = Blueprint("user", __name__, url_prefix="/user")


@user.errorhandler(Exception)
def handle_error(error):
    status_code = 500  # Default status code for Internal Server Error
    message = str(error)

    # Log the error for debugging
    print(f"Error: {error}")

    # Check if the exception has a status_code attribute
    if hasattr(error, 'status_code'):
        status_code = error.status_code

    type = error.__class__.__name__,

    return type, status_code


@user.route('/view')
def view_user():
    from models.user_model import UserModel  # noqa
    res = UserModel.query.all()
    result = []
    for i in res:
        event_dict = {"user_id": i.user_id,
                      "user_name": i.username,
                      "uoft_email": i.uoft_email,
                      "organizational_role": i.organizational_role,
                      "enrolled_time": i.enrolled_time,
                      "au": i.authenticated,
                      }
        result.append(event_dict)
    return jsonify({"code": 200, "msg": "OK", "data": result})


@user.route("register", methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('uoftEmail')
        password = data.get('password')
        student_id = data.get('uoftStudentId')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        department = data.get('department')
        enrolled_time = data.get('enrolledTime')
        organizational_role = data.get('organizationalRole')

        # Validate required fields
        if not username or not email or not password:
            return jsonify({"code": 400, "error": "username,email,password fields are required"}), 400

        # Check if the username is already taken
        from backend.models.user_model import UserModel  # noqa
        existing_user = UserModel.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"code": 401, "error": "Username already exists"}), 401

        # Hash the password
        from backend import bcrypt  # noqa
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        # Create a new user
        new_user = UserModel(username=username, uoft_email=email, password_hash=hashed_password,
                             uoft_student_id=student_id, first_name=first_name, last_name=last_name,
                             department=department, enrolled_time=enrolled_time,
                             authenticated=True, organizational_role=organizational_role)
        from backend import db  # noqa
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"code": 200, "msg": "Registration successful"}), 200
    except Exception as e:
        response, status_code = handle_error(e)
        return jsonify({"code": status_code, "error": response}), status_code


@user.route("/login", methods=['POST'])
def login():
    try:
        # Check the hash
        username = request.json["username"]
        password = request.json["password"]
        from models.user_model import UserModel  # noqa
        user = UserModel.query.filter_by(username=username).first()
        if user and user.is_authenticated:
            from backend import bcrypt  # noqa
            if bcrypt.check_password_hash(user.password_hash, password):
                login_user(user)
                return jsonify({"code": 200, "msg": "Login Succesfull."}), 200
            else:
                return jsonify({"error": "Wrong Password - Try Again!"}), 401
        else:
            return jsonify({"error": "Unauthorized Access"}), 409
    except Exception as e:
        response, status_code = handle_error(e)
        return jsonify(response), status_code


@user.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!  Thanks For Stopping By...")
    return jsonify({"code": 200, "msg": "Log out Succesfully."}), 200
