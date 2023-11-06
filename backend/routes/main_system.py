from flask import Blueprint, jsonify, request
from sqlalchemy import text

# from routes import main_sys
# from Models.main_system_model import MainSysModel

#from Models.main_system_model import MainSysModel

# from backend.Models.main_system_model import MainSysModel
# from .Models.main_system_model import MainSysModel

main_sys = Blueprint("main_sys", __name__, url_prefix="/main_sys")



def get_event_info(event_id):
    from models.event_info_model import EventInfoModel  # noqa
    sql = text("select * from event_info_table where event_id = :event_id")
    return EventInfoModel.query.from_statement(sql.bindparams(event_id=event_id)).all()


@main_sys.route('/', methods=["GET"])
def event_general_info():
    event_id = request.args.get('event_id')
    data_model = get_event_info(event_id)
    print(data_model)
    data = {
        'event_id': data_model[0].event_id,
        'event_time': data_model[0].event_time,
        'event_description': data_model[0].event_description,
        'number_rater': data_model[0].number_rater,
        'average_rating': data_model[0].average_rating
    }
    return jsonify({"code": 200, "msg": "success", "data": data})


@main_sys.route('/filter', methods=["GET"])
def filter_event():
    filter_title = request.args.get('title')
    if isinstance(filter_title, str) is False:
        return jsonify({"code": 401, "msg": "Illegal input", "data": []}), 401

    if not filter_title:
        return jsonify({"code": 401, "msg": "No filter applied", "data": []}), 401

    if filter_title not in ["sport", "art", "travel", "cooking"]:
        return jsonify({"code": 401, "msg": "filter does not exist", "data": []}), 401
    # filter_list = filter_title.split(",")
    data = filter_event_impl(filter_title)
    return jsonify({"code": 200, "msg": "OK", "data": data}), 200


def filter_event_impl(filter_list):
    from models.event_filter_model import EventFilerModel # noqa
    from models.event_info_model import EventInfoModel # noqa
    from backend import db # noqa
    condition = filter_list

    res = db.session.query(EventInfoModel.event_id, EventInfoModel.event_name,
                           EventInfoModel.event_desc, EventInfoModel.organizer,
                           EventFilerModel.filter).join(EventFilerModel, EventInfoModel.event_id == EventFilerModel.event_id).\
        filter(EventFilerModel.filter == condition).all()

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



@main_sys.route('/add_filter', methods=['GET'])
def add_event_filter():
    event_id = request.args.get('event_id')
    filter_name = request.args.get('filter_name')

    # from .Models.main_system_model import MainSysModel
    status, e = insert_event_impl(event_id, filter_name)
    if status is False:
        return jsonify({"code": 200, "msg": "INSERTION FAILED", "data": e}), 200

    return jsonify({"code": 200, "msg": "INSERTED", "data": []}), 200


def insert_new_event(event_id, name, desc, organizer):
    from models.event_info_model import EventInfoModel  # noqa
    from backend import db

    new_event_info = EventInfoModel(event_id, name, desc, organizer)
    try:
        db.session.add(new_event_info)
        db.session.commit()
    except Exception as e:
        return False, str(e)

    return True, ""


@main_sys.route('/view_events')
def view_event():
    data = view_event_impl()
    return jsonify({"code": 200, "msg": "OK", "data": data}), 200


def view_event_impl():
    sql = text("select * from event_info_table")
    from models.event_info_model import EventInfoModel  # noqa
    res = EventInfoModel.query.from_statement(sql).all()
    result = []
    for i in res:
        event_dict = {"event_id": i.event_id,
                      "event_name": i.event_name,
                      "event_desc": i.event_desc,
                      "organizer": i.organizer}
        result.append(event_dict)
    return result

@main_sys.route('/view_filter')
def view_filter():
    sql = text("select * from event_filter_table")
    from models.event_filter_model import EventFilerModel # noqa
    res = EventFilerModel.query.from_statement(sql).all()
    result = []
    for i in res:
        res_dict = {"event_id": i.event_id,
                    "filter": i.filter}
        result.append(res_dict)
    return jsonify({"code": 200, "msg": "OK", "data": result}), 200



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


def insert_event_impl(event_id, filter_name):
    # from models.Event_model import db  # noqa
    # sql_conn = db
    from models.event_filter_model import EventFilerModel  # noqa
    from backend import db
    new_event_filter = EventFilerModel(event_id, filter_name)
    try:
        db.session.add(new_event_filter)
        db.session.commit()
    except Exception as e:
        return False, str(e)

    return True, ""









