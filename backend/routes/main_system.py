from flask import Blueprint, jsonify, request

#from Models.main_system_model import MainSysModel

# from backend.Models.main_system_model import MainSysModel

main_sys = Blueprint("main_sys", __name__, url_prefix="/main_sys")
from .Models.main_system_model import MainSysModel

@main_sys.route('/filter', methods=["GET"])
def filter_event():
    filter_title = request.args.get('title')
    if isinstance(filter_title, str) is False:
        return jsonify({"code": 401, "msg": "Illegal input", "data": []}), 401

    if not filter_title:
        return jsonify({"code": 200, "msg": "No filter applied", "data": []}), 200

    if filter_title not in ["sport", "art", "travel", "cooking"]:
        return jsonify({"code": 200, "msg": "filter does not exist", "data": []}), 200
    #filter_list = filter_title.split(",")
    main_obj = MainSysModel()
    data = main_obj.filter_event(filter_title)
    return jsonify({"code": 200, "msg": "OK", "data": data}), 200


'''
test db purposes
'''
@main_sys.route('/add_filter', methods=['GET'])
def add_event_filter():
    event_id = request.args.get('event_id')
    filter_name = request.args.get('filter_name')

    #from .Models.main_system_model import MainSysModel
    main_obj = MainSysModel()
    status, e = main_obj.insert_event(event_id, filter_name)
    if status is False:
        return jsonify({"code": 200, "msg": "INSERTION FAILED", "data": e}), 200

    return jsonify({"code": 200, "msg": "INSERTED", "data": []}), 200


