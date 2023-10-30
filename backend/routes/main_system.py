from flask import Blueprint, jsonify, request

main_sys = Blueprint("main_sys", __name__, url_prefix="/main_sys")


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

    from backend.Models.main_system_model import MainSysModel
    main_obj = MainSysModel()
    data = main_obj.filter_event(filter_title)
    return jsonify({"code": 200, "msg": "OK", "data": data}), 200

@main_sys.route('/search', methods=["GET"])
def search():
    data = request.get_json()
    query = data.get('Eventname')
   
    if query:
        return jsonify({"code": 302, "Eventname": query}), 302
        
    return jsonify({"code": 405, "Eventname": "No events are found"}), 405
