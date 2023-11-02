from flask import Blueprint, jsonify, request
from sqlalchemy import text

# from routes import main_sys
# from Models.main_system_model import MainSysModel
# from backend.Models.main_system_model import MainSysModel
# from .Models.main_system_model import MainSysModel

main_sys = Blueprint("main_sys", __name__, url_prefix="/main_sys")


def filter_event_impl(filter_list):
    from models.event_filter import EventFilerDB # noqa
    from models.event_info import EventInfoDB # noqa
    from backend import db # noqa
    condition = filter_list

    res = db.session.query(EventInfoDB.event_id, EventInfoDB.event_name,
                           EventInfoDB.event_desc, EventInfoDB.organizer,
                           EventFilerDB.filter).join(EventFilerDB, EventInfoDB.event_id == EventFilerDB.event_id).\
        filter(EventFilerDB.filter == condition).all()

    result = []
    for i in res:
        event_dict = {"event_id": i[0],
                      "event_name": i[1],
                      "description": i[2],
                      "organizer": i[3],
                      "filter": i[4]
                      }
        result.append(event_dict)
    return result


def insert_event_impl(event_id, filter_name):
    # from models.Event_model import db  # noqa
    # sql_conn = db
    from models.event_filter import EventFilerDB  # noqa
    from backend import db
    new_event_filter = EventFilerDB(event_id, filter_name)
    try:
        db.session.add(new_event_filter)
        db.session.commit()
    except Exception as e:
        return False, str(e)

    return True, ""


def view_event_impl():
    sql = text("select * from event_info")
    from models.event_info import EventInfoDB  # noqa
    res = EventInfoDB.query.from_statement(sql).all()
    result = []
    for i in res:
        event_dict = {"event_id": i.event_id,
                      "event_name": i.event_name,
                      "event_desc": i.event_desc,
                      "organizer": i.organizer}
        result.append(event_dict)
    return result


def insert_new_event(event_id, name, desc, organizer):
    from models.event_info import EventInfoDB  # noqa
    from backend import db

    new_event_info = EventInfoDB(event_id, name, desc, organizer)
    try:
        db.session.add(new_event_info)
        db.session.commit()
    except Exception as e:
        return False, str(e)

    return True, ""

@main_sys.route('/filter', methods=["GET"])
def filter_event():
    filter_title = request.args.get('title')
    if isinstance(filter_title, str) is False:
        return jsonify({"code": 401, "msg": "Illegal input", "data": []}), 401

    if not filter_title:
        return jsonify({"code": 200, "msg": "No filter applied", "data": []}), 200

    if filter_title not in ["sport", "art", "travel", "cooking"]:
        return jsonify({"code": 200, "msg": "filter does not exist", "data": []}), 200
    # filter_list = filter_title.split(",")
    data = filter_event_impl(filter_title)
    return jsonify({"code": 200, "msg": "OK", "data": data}), 200

@main_sys.route('/add_filter', methods=['GET'])
def add_event_filter():
    event_id = request.args.get('event_id')
    filter_name = request.args.get('filter_name')

    # from .Models.main_system_model import MainSysModel
    status, e = insert_event_impl(event_id, filter_name)
    if status is False:
        return jsonify({"code": 200, "msg": "INSERTION FAILED", "data": e}), 200

    return jsonify({"code": 200, "msg": "INSERTED", "data": []}), 200



@main_sys.route('/view_events')
def view_event():
    data = view_event_impl()
    return jsonify({"code": 200, "msg": "OK", "data": data}), 200


@main_sys.route("/add_event", methods=['GET'])
def add_event_info():
    event_id = request.args.get('event_id')
    event_name = request.args.get('name')
    desc = request.args.get('desc')
    organizer = request.args.get('organizer')

    status, e = insert_new_event(event_id, event_name, desc, organizer)
    if status is False:
        return jsonify({"code": 200, "msg": "INSERTION FAILED", "data": e}), 200

    return jsonify({"code": 200, "msg": "INSERTED", "data": []}), 200

