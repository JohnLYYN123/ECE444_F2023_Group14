from flask import Blueprint, flash, jsonify, render_template, request, g
from functools import wraps
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import URLSafeTimedSerializer as Serializer
import traceback

TWO_WEEKS = 1209600


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


# Endpoint to get enrolled events based on the type (upcoming/past)
@enrollment.route('/enrollment/<int:id>?type=${viewing_type}', methods=['GET'])
def get_enrolled_events():
    from models.user_enroll_event_model import UserEnrollEventModel
    from backend import db
    from backend.models.user_model import UserModel
    user = UserModel.query.filter_by(
        user_id=g.current_user["user_id"]).first()
    
    enrollments = UserEnrollEventModel.query.filter_by(user_id=user).all()

    viewing_type = request.args.get('type', 'upcoming')

    now = datetime.now()

    if viewing_type == 'upcoming':
        filtered_events = [event for event in enrollments if  datetime.strptime(enrollments, '%Y-%m-%d') >= now]
    else:
        filtered_events = [event for event in enrollments if  datetime.strptime(enrollments, '%Y-%m-%d') < now]

    return jsonify(filtered_events)
