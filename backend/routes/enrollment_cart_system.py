from flask import Blueprint, flash, jsonify, render_template, request, g
from functools import wraps
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import Blueprint, flash, jsonify, make_response, render_template, request, g
from datetime import datetime

TWO_WEEKS = 1209600
enroll = Blueprint("enroll", __name__, url_prefix="/enroll")


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


@enroll.errorhandler(Exception)
def handle_error(error):
    status_code = 500  # Default status code for Internal Server Error
    message = str(error)
    # Check if the exception has a status_code attribute
    if hasattr(error, 'status_code'):
        status_code = error.status_code
    type = error.__class__.__name__,
    return type, status_code


@enroll.route("/", methods=['GET'])
@requires_auth
def check_enrolled_events():
    try:
        from backend.models.user_model import UserModel
        if g.current_user["user_id"] is None:
            return jsonify({"code": 400, "error": "No current user"}), 400
        # find the user
        user = UserModel.query.filter_by(
            user_id=g.current_user["user_id"]).first()
        # Check if the user exists
        if user is None:
            return jsonify({"code": 404, "error": "User not found"}), 404
        from backend.models.user_enroll_event_model import UserEnrollEventModel
        all_enrolled_events = UserEnrollEventModel.query.filter_by(
            user_id=g.current_user["user_id"]).all()
        # Check if there are no enrolled events
        if not all_enrolled_events:
            return jsonify({"code": 404, "error": "No enrolled events for the user"}), 404
        enrolled_event_ids = []
        for enrolled_event in all_enrolled_events:
            enrolled_event_ids.append(enrolled_event.event_id)
        from backend.models.event_info_model import EventInfoModel
        all_event_models = EventInfoModel.query.filter(
            EventInfoModel.event_id.in_(enrolled_event_ids)).all()
        # event name and event time is required fileds, don't need to check
        event_details = [{"event_name": event.event_name,
                          "event_time": event.event_time,
                          "event_address": event.address if event.address else "Not Known Yet",
                          "event_id": event.event_id} for event in all_event_models]
        current_datetime = datetime.now()
        passed_events = []
        future_events = []
        for event in event_details:
            event_time = event['event_time']
            if event_time <= current_datetime:
                passed_events.append(event)
            else:
                future_events.append(event)
        return jsonify({"code": 200, "future": future_events, "past": passed_events}), 200
    except Exception as e:
        response, status_code = handle_error(e)
        return jsonify({"code": status_code, "error": response}), status_code
