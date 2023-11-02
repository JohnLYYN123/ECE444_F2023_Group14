from flask import jsonify, render_template, request, redirect, url_for, Blueprint
from sqlalchemy import text

detail = Blueprint("detail", __name__, url_prefix="/detail")


@detail.route("/", methods=['GET'])
def display():
    view_event_id = request.args.get("event_id")
    data = view_comment_impl(view_event_id)
    return jsonify({"code": 200, "msg": "OK", "data": data}), 200

def view_comment_impl(view_event_id):
    sql = text("select * from event_info")
    from models.review_rating import ReviewRatingDB  # noqa
    sql = text("select * from review_rating where filter = :cond")
    res = ReviewRatingDB.query.from_statement(sql.bindparams(cond = view_event_id)).all()
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
    review_time = request.args.get('time')

    status, e = insert_new_event(view_event_id, review_id, review_user, review_comment, review_time)
    if status is False:
        return jsonify({"code": 200, "msg": "INSERTION FAILED", "data": e}), 200

    return jsonify({"code": 200, "msg": "INSERTED", "data": []}), 200

def insert_new_event(view_event_id, review_id, review_user, review_comment, review_time):
    from models.review_rating import ReviewRatingDB  # noqa
    from backend import db

    new_event_info = ReviewRatingDB({"event_id": view_event_id,
                                    "review_id": review_id,
                                    "review_user": review_user,
                                    "review_comment": review_comment,
                                    "review_time": review_time})
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

    if isinstance(event_id, int) is False:
        return jsonify({"code": 401, "msg": "Illegal input type", "data": []}), 401

    if not event_id:
        return jsonify({"code": 401, "msg": "Illegal input", "data": []}), 401





