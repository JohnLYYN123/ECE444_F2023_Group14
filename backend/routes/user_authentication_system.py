from sqlalchemy import text
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for, g
from functools import wraps
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import URLSafeTimedSerializer as Serializer

user = Blueprint("user", __name__, url_prefix="/user")


TWO_WEEKS = 1209600

# Reference: https://github.com/dternyak/React-Redux-Flask/tree/master
def generate_token(user):
    from backend import app  # noqa
    s = Serializer(app.config['SECRET_KEY'])
    token = s.dumps({
        'user_id': user.user_id,
        'uoft_email': user.uoft_email,
    }).encode().decode('utf-8')
    return token

# Reference: https://github.com/dternyak/React-Redux-Flask/tree/master
def verify_token(token):
    from backend import app  # noqa
    s = Serializer(app.config['SECRET_KEY'])
    try:
        # Verify the token's expiration
        data = s.loads(token, max_age=TWO_WEEKS)
    except (BadSignature, SignatureExpired):
        return None
    return data

# Reference: https://github.com/dternyak/React-Redux-Flask/tree/master
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token:
            string_token = token.encode('ascii', 'ignore')
            user = verify_token(string_token)
            if user:
                g.current_user = user
                return f(*args, **kwargs)

        return jsonify({"code": 401, "error": "Authentication is required to access this resource"}), 401

    return decorated


@user.errorhandler(Exception)
def handle_error(error):
    status_code = 500  # Default status code for Internal Server Error

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
                      }
        result.append(event_dict)
    return jsonify({"code": 200, "msg": "OK", "data": result})


@user.route("register", methods=['POST'])
def register():
    from backend.logs.admin import setup_logger

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

        if 'utoronto' not in email:
            return jsonify({"code": 400, "error": "Email should contain 'utoronto'"}), 400

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
                             organizational_role=organizational_role)
        from backend import db  # noqa
        db.session.add(new_user)
        db.session.commit()
        token = generate_token(new_user)
        return jsonify({"code": 200, "token": token})
    except Exception as e:
        operation_log = setup_logger('user.register')
        operation_log.error('%s', e)
        response, status_code = handle_error(e)
        return jsonify({"code": status_code, "error": response}), status_code


@user.route("/login", methods=['GET', 'POST'])
def login():
    from backend.logs.admin import setup_logger

    try:
        # Check the hash
        username = request.json["username"]
        password = request.json["password"]
        from backend.models.user_model import UserModel  # noqa
        user = UserModel.query.filter_by(username=username).first()
        if user:
            from backend import bcrypt  # noqa
            if bcrypt.check_password_hash(user.password_hash, password):
                token = generate_token(user)
                verify_token(token)
                return jsonify({"code": 200, "token": token}), 200
            else:
                return jsonify({"code": 401, "error": "Wrong Password - Try Again!"}), 401
        else:
            return jsonify({"code": 409, "error": "Please register an account first!"}), 409
    except Exception as e:
        operation_log = setup_logger('user.login')
        operation_log.error('%s', e)
        response, status_code = handle_error(e)
        return jsonify({"code": status_code, "error": response}), status_code


@user.route('/logout', methods=['POST', 'GET'])
@requires_auth
def logout():
    from backend.logs.admin import setup_logger

    try:
        return jsonify({"code": 200, "msg": "Log out Succesfully."}), 200
    except Exception as e:
        operation_log = setup_logger('user.logout')
        operation_log.error('%s', e)
        return jsonify({"code": 400, "error": str(e)}), 400
