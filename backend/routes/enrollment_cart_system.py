from flask import Blueprint, flash, jsonify, render_template, request, g
from functools import wraps
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import URLSafeTimedSerializer as Serializer
import traceback

TWO_WEEKS = 1209600

enrollment = Blueprint("enrollment", __name__, url_prefix="/enrollment")

def verify_token(token):
    from backend import app  # noqa
    s = Serializer(app.config['SECRET_KEY'])
    try:
        # Verify the token's expiration
        data = s.loads(token, max_age=TWO_WEEKS)
    except (BadSignature, SignatureExpired):
        return None
    return data


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

        return jsonify(message="Authentication is required to access this resource"), 401

    return decorated

@enrollment.route('/enrollment/<int:id>/', methods=['GET'])
# Show the enrollment events
def show_event():
    from routes.main_system import view_detail
    from models.user_enroll_event_model import UserEnrollEventModel
    from backend import db

    from backend.models.user_model import UserModel
    user = UserModel.query.filter_by(
        user_id=g.current_user["user_id"]).first()
    
    enrollments = UserEnrollEventModel.query.filter_by(user_id=user).all()
    for enrollment in enrollments:
        enrolled_eventid = [enrollment.event_id]
        EnrolledEvent = view_detail(enrolled_eventid)
        return jsonify({"code": 200, "msg": "OK", "data": EnrolledEvent}), 200
    

@enrollment.route("/register/<int:id>/", methods=['POST', 'GET'])
def enrol(id):
    from models.user_enroll_event_model import UserEnrollEventModel
    from backend import db

    from backend.models.user_model import UserModel
    user = UserModel.query.filter_by(
        user_id=g.current_user["user_id"]).first()

    from backend.models.event_info_model import EventInfoModel
    current_event = EventInfoModel.query.filter_by(event_id=id).first()

    new_enrollment = UserEnrollEventModel(user_id=user, event_id=current_event)
    try:
        db.session.add(new_enrollment)
        db.session.commit()
    except Exception as e:
        return False, str(e)

    return True, ""
