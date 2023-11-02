from flask import jsonify, render_template, request, redirect, url_for, Blueprint

detail = Blueprint("detail", __name__, url_prefix="/detail")


@detail.route("/", methods=['POST'])
def display():
    # page not built yet, return to index with nothing for now
    return render_template("index.html")


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
        return jsonify({"code": 401, "msg": "empty input date when should not be empty", "data": []}), 401

    if event_id < 0:
        return jsonify({"code": 401, "msg": "Negative event_id is not allowed", "data": []}), 401

    result = view_detail_impl(event_id)
    return jsonify({"code": 200, "msg": "OK", "data": result}), 200



def view_detail_impl(event_id):
    result = []
    review_res = []
    from backend import db # noqa
    from models.review_rating import ReviewRatingDB # noqa



    return result


