import traceback
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from functools import wraps
from flask import Blueprint, flash, jsonify, render_template, request, g
from flask import jsonify, render_template, request, redirect, url_for, Blueprint
from sqlalchemy import text

detail = Blueprint("detail", __name__, url_prefix="/detail")

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

@detail.route("/display_comment", methods=['GET'])
def display():
    view_event_id = request.args.get("event_id")
    data = view_comment_impl(view_event_id)
    return jsonify({"code": 200, "msg": "OK", "data": data}), 200


def view_comment_impl(view_event_id):
    sql = text("select * from event_info")
    from models.review_rating_model import ReviewRatingDB  # noqa
    sql = text("select * from review_rating where event_id = :cond")
    res = ReviewRatingDB.query.from_statement(
        sql.bindparams(cond=view_event_id)).all()
    result = []
    for i in res:
        event_dict = {"review_id": i.review_id,
                      "review_user": i.review_user,
                      "review_comment": i.review_comment,
                      "review_time": i.review_time}
        result.append(event_dict)
    return result


@detail.route("/add_comment", methods=['GET', 'POST'])
def add_event_info():
    event_id = request.args.get('event_id')
    data = request.json
    review_user = data.get('username')
    review_comment = data.get('comment')
    rating = data.get('rating')

    response_data = {
        'username': review_user,
        'comment': review_comment,
        'rating': rating,
    }

    status, e = insert_new_event(
        event_id, review_user, review_comment, rating)
    if status is False:
        return jsonify({"code": 406, "msg": "INSERTION FAILED", "response_data": e}), 406

    return jsonify({"code": 200, "msg": "INSERTED", "response_data": response_data}), 200


def insert_new_event(view_event_id, review_id, review_user, review_comment, rating):
    from models.review_rating_model import ReviewRatingDB  # noqa
    from backend import db

    new_event_info = ReviewRatingDB({"event_id": view_event_id,
                                    "review_id": None,
                                     "review_user": review_user,
                                     "review_comment": review_comment,
                                     "rating": rating,
                                     "review_time": None})
    try:
        db.session.add(new_event_info)
        db.session.commit()
    except Exception as e:
        return False, str(e)

    return True, ""


@detail.route("/view_detail", methods=["GET"])
def view_detail():
    event_id = request.args.get("event_id")

    # if isinstance(event_id, int) is False:
    #    return jsonify({"code": 401, "msg": "Illegal input type", "data": []}), 401

    if not event_id:
        return jsonify({"code": 401, "msg": "empty input date when should not be empty", "data": []}), 401

    # if event_id < 0:
     #   return jsonify({"code": 401, "msg": "Negative event_id is not allowed", "data": []}), 401

    result = view_detail_impl(event_id)
    return jsonify({"code": 200, "msg": "OK", "data": result}), 200


def view_detail_impl(event_id):
    result = []
    review_res = []
    from backend import db  # noqa
    from models.review_rating_model import ReviewRatingDB  # noqa
    return result

# view to check if insert into the table


@detail.route('/user/view')
def view_host_table():
    sql = text("select * from user_enroll_event_table;")
    from backend.models.user_enroll_event_model import UserEnrollEventModel  # noqa
    res = UserEnrollEventModel.query.from_statement(sql).all()
    result = []
    for i in res:
        event_dict = {"user_id": i.user_id,
                      "event_id": i.event_id,
                      }
        result.append(event_dict)
    return jsonify({"code": 200, "msg": "OK", "data": result}), 200

# user register event, add to backend/models/user_enroll_event_model.py


@detail.route("/register/<int:id>/", methods=['POST', 'GET'])
@requires_auth
def user_register_event(id):
    from backend.models.user_model import UserModel
    user = UserModel.query.filter_by(
        user_id=g.current_user["user_id"]).first()
    from backend.models.host_event_model import HostEventModel
    is_host_of_the_event = HostEventModel.query.filter_by(
        host_id=g.current_user["user_id"], event_id=id).first()
    from backend.models.event_info_model import EventInfoModel
    current_event = EventInfoModel.query.filter_by(event_id=id).first()
    # current user is not the host of the event
    if current_event and user:
        if not is_host_of_the_event:
            try:
                from backend.models.user_enroll_event_model import UserEnrollEventModel  # noqa
                new_participant = UserEnrollEventModel(
                    user_id=int(user.user_id),
                    event_id=int(current_event.event_id),
                )
                participants = UserEnrollEventModel.query.all()
                duplicate_insert_participation = False

                for participant in participants:
                    if participant == new_participant:
                        duplicate_insert_participation = True

                if duplicate_insert_participation:
                    return jsonify({"code": 409, "error": "You have already registered for the event."}), 409
                from backend import db  # noqa
                db.session.add(new_participant)
                db.session.commit()
                return jsonify({"code": 200, "msg": "Congrats, you successfully registered for the event."}), 200

            except Exception as e:
                status_code = 500
                if hasattr(e, 'status_code'):
                    status_code = e.status_code
                type = e.__class__.__name__,
                return jsonify({"code": status_code, "error": type}), status_code
        return jsonify({"code": 409, "error": "You are the host of the event."}), 409
    return jsonify({"code": 409, "error": "Selected event or your account does not exist."}), 409
