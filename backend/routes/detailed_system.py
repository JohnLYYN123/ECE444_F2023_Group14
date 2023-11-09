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


@detail.route("/", methods=['GET'])
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


@detail.route("/add_comment", methods=['GET'])
def add_event_info():
    view_event_id = request.args.get('event_id')
    review_id = request.args.get('review_id')
    review_user = request.args.get('user')
    review_comment = request.args.get('comment')
    rating = request.args.get('rate')

    status, e = insert_new_event(
        view_event_id, review_id, review_user, review_comment, rating)
    if status is False:
        return jsonify({"code": 200, "msg": "INSERTION FAILED", "data": e}), 200

    return jsonify({"code": 200, "msg": "INSERTED", "data": []}), 200


def insert_new_event(view_event_id, review_id, review_user, review_comment, rating):
    from models.review_rating_model import ReviewRatingDB  # noqa
    from backend import db

    new_event_info = ReviewRatingDB({"event_id": view_event_id,
                                    "review_id": review_id,
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


@detail.route("/add", methods=['POST', 'GET'])
def add_entry():
    """Adds new comment to the comment section."""
    data = request.get_json()
    comment_title = data.get('Title')
    comment_content = data.get('Content')

    if (comment_title) and (comment_content):
        return redirect(url_for("detail.display"))

    return jsonify({'message': 'Empty field not allowed'}), 406


@detail.route("/view_detail", methods=["GET"])
def view_detail():
    event_id = request.args.get("event_id")

    # if isinstance(event_id, int) is False:
    #    return jsonify({"code": 401, "msg": "Illegal input type", "data": []}), 401

    if not event_id:
        return jsonify({"code": 401, "msg": "empty input date when should not be empty", "data": []}), 401

    if int(event_id) < 0:
        return jsonify({"code": 401, "msg": "Negative event_id is not allowed", "data": []}), 401

    result = view_detail_impl(event_id)
    return jsonify({"code": 200, "msg": "OK", "data": result}), 200


def view_detail_impl(event_id):
    result_dict = {}
    from backend import db  # noqa
    from backend.models.event_info_model import EventInfoModel, ClubInfoModel  # noqa

    idx = event_id
    sql = text("select * from event_info_table where event_id = :cond ")
    event_info = EventInfoModel.query.from_statement(sql.bindparams(cond=idx)).all()

    # event_id is primary, and thus should be unique in the DB
    event_info = event_info[0]
    club_id = event_info.club_id
    sql = text("select * from club_info_table where club_id = :cond ")
    club_info = ClubInfoModel.query.from_statement(sql.bindparams(cond=club_id)).all()
    club_info = club_info[0]
    event_dict = {
        "event_id": event_info.event_id,
        "event_name": event_info.event_name,
        "event_time": event_info.event_time,
        "number_rater": event_info.number_rater,
        "average_rating": event_info.average_rating,
        "event_description": event_info.event_description,
        "event_image": event_info.event_image,
        "position_address": event_info.position_addre,
        "address": event_info.address,
        "charge": event_info.charge,
        "club_id": event_info.club_id,
        "club_name": club_info.club_name,
        "host_name": club_info.host_name,
        "club_desc": club_info.description
    }

    sql = text("select user_id, first_name from user_table ")
    from backend.models.user_model import UserModel
    user_info = UserModel.query.from_statement(sql).all()

    user_dict = {}
    for user in user_info:
        user_dict[user.user_id] = user.first_name

    # get reviews of the event (correspond to the event id)
    sql = text("select * from review_rating_table where event_id = :cond ")
    from backend.models.review_rating_model import ReviewRatingModel
    review_info = ReviewRatingModel.query.from_statement(sql.bindparams(cond=idx)).all()

    num_review = len(review_info)
    review_dict = {}
    total_rating = 0
    avg_rating = 0.0
    review_detail = []
    if num_review != 0:
        for rev in review_info:
            rev_dict = {
                "review_user": user_dict[rev.review_user],
                "rating": rev.rating,
                "review_comment": rev.review_comment,
                "review_time": rev.review_time
            }
            review_detail.append(rev_dict)
            total_rating += rev.rating

        avg_rating = round(total_rating/num_review, 1)

    review_dict["number_review"] = num_review
    review_dict["avg_rating"] = avg_rating
    review_dict["review_detail"] = review_detail

    if event_dict["average_rating"] != avg_rating:
        event_dict["average_rating"] = avg_rating

    if event_dict["number_rater"] != num_review:
        event_dict["number_rater"] = num_review

    result_dict["event_info"] = event_dict
    result_dict["review_info"] = review_dict
    return result_dict


@detail.route('/review_view')
def review_rating_view():
    result = []
    sql = text("select * from review_rating_table ")
    from backend.models.review_rating_model import ReviewRatingModel
    res = ReviewRatingModel.query.from_statement(sql).all()
    for i in res:
        review_dict = {
            "review_id": i.review_id,
            "event_id": i.event_id,
            "review_user": i.review_user,
            "rating": i.rating,
            "review_comment": i.review_comment,
            "review_time": i.review_time
        }
        result.append(review_dict)
    return jsonify({"code": 200, "msg": "OK", "data": result}), 200

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
