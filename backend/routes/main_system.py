from flask import Blueprint, flash, jsonify, render_template, request, g
from sqlalchemy import text
from datetime import datetime
from functools import wraps
from itsdangerous import SignatureExpired, BadSignature
from itsdangerous import URLSafeTimedSerializer as Serializer
import os
from pathlib import Path
from werkzeug.utils import secure_filename


main_sys = Blueprint("main_sys", __name__, url_prefix="/main_sys")

TWO_WEEKS = 1209600


def get_filter_info_by_event_id(event_id):
    from backend.models.event_filter_model import EventFilerModel  # noqa
    from backend import db  # noqa
    # sql = text("select filter from event_filter_table")
    rows = db.session.query(EventFilerModel.filter).filter(
        EventFilerModel.event_id == event_id).all()
    return [row[0] for row in rows]


def event_info_res_provider(data_model, event_id):
    filter_info = get_filter_info_by_event_id(event_id)
    print('res', event_id)
    print('res', data_model)
    print('res filter', filter_info)
    return {
        'event_id': event_id,
        'event_name': data_model.event_name,
        'event_time': data_model.event_time,
        'average_rating': data_model.average_rating,
        'event_image': data_model.event_image,
        'filter_info': filter_info,
    }


def get_event_info_all():
    from backend.models.event_info_model import EventInfoModel  # noqa
    sql = text(
        "select event_id, event_name, event_time, average_rating from event_info_table")
    data_models = EventInfoModel.query.from_statement(sql).all()
    print('all', data_models)
    return [event_info_res_provider(data, data.event_id) for data in data_models]


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

        return jsonify({"code": 401, "error": "Authentication is required to access this resource"}), 401

    return decorated


def get_event_info(event_id):
    from backend.models.event_info_model import EventInfoModel  # noqa
    sql = text(
        "select event_id, event_name, event_time, average_rating from event_info_table where event_id = :event_id")
    data_model = EventInfoModel.query.from_statement(
        sql.bindparams(event_id=event_id)).all()

    return event_info_res_provider(data_model[0], event_id) if len(data_model) > 0 else {}


@main_sys.route('/', methods=["GET"])
@requires_auth
def event_general_info():
    from backend.models.user_model import UserModel
    if g.current_user["user_id"] is None:
        return jsonify({"code": 400, "error": "No current user"}), 400
    # find the user
    user = UserModel.query.filter_by(
        user_id=g.current_user["user_id"]).first()
    # Check if the user exists
    if user is None:
        return jsonify({"code": 404, "error": "User not found"}), 404
    event_id = request.args.get('event_id')
    if event_id is '':
        return jsonify({"code": 200, "msg": "Event id is empty", "data": []}), 200
    data = get_event_info_all() if event_id == '-1' else get_event_info(event_id)
    print('data', data)
    if len(data) == 0:
        return jsonify({"code": 401, "msg": "Event does not exist", "data": []}), 401

    return jsonify({"code": 200, "msg": "success", "data": data})


def search_event_info(search_string):
    from backend import db  # noqa
    from backend.models.event_info_model import EventInfoModel  # noqa
    search_text = "%{}%".format(search_string)
    print('search_text', search_text)
    data_model = db.session.query(
        EventInfoModel.event_id,
        EventInfoModel.event_name,
        EventInfoModel.event_time,
        EventInfoModel.average_rating,
        EventInfoModel.event_image
    ).filter(EventInfoModel.event_name.like(search_text)).all()
    print(data_model)
    return [event_info_res_provider(data, data.event_id) for data in data_model]


@main_sys.route('/search', methods=["GET"])
@requires_auth
def search_event():

    # check for user authentication
    from backend.models.user_model import UserModel
    if g.current_user["user_id"] is None:
        return jsonify({"code": 400, "error": "No current user"}), 400
    # find the user
    user = UserModel.query.filter_by(
        user_id=g.current_user["user_id"]).first()
    # Check if the user exists
    if user is None:
        return jsonify({"code": 404, "error": "User not found"}), 404

    search_string = request.args.get('value')
    data = search_event_info(search_string)

    return jsonify({"code": 200, "msg": "success", "data": data})


@main_sys.route('/filter', methods=["GET"])
@requires_auth
def filter_event():
    # user authentication
    from backend.models.user_model import UserModel
    if g.current_user["user_id"] is None:
        return jsonify({"code": 400, "error": "No current user"}), 400

    user = UserModel.query.filter_by(user_id=g.current_user["user_id"]).first()
    if user is None:
        return jsonify({"code": 404, "error": "User not found"}), 404

    filter_title = request.args.get('title')
    search_val = request.args.get('search_value')
    if isinstance(filter_title, str) is False:
        return jsonify({"code": 401, "msg": "Illegal input", "data": []}), 401

    if not filter_title:
        return jsonify({"code": 401, "msg": "No filter applied", "data": []}), 401

    if filter_title not in ["sport", "art", "travel", "cooking"]:
        return jsonify({"code": 401, "msg": "filter does not exist", "data": []}), 401
    # filter_list = filter_title.split(",")

    if not search_val:
        data = filter_event_impl(filter_title)
    else:
        if isinstance(search_val, str) is False:
            return jsonify({"code": 401, "msg": "Illegal input for search_val", "data": []}), 401

        data = filter_event_impl(filter_title, search_val)
    return jsonify({"code": 200, "msg": "OK", "data": data}), 200


def filter_event_impl(filter_title, search_val=''):
    from backend.models.event_filter_model import EventFilerModel  # noqa
    from backend.models.event_info_model import EventInfoModel, ClubInfoModel  # noqa
    from backend import db  # noqa
    condition = filter_title

    if not search_val:
        res = db.session.query(EventInfoModel.event_id, EventInfoModel.event_name,
                               EventInfoModel.event_description, EventInfoModel.club_id,
                               EventInfoModel.average_rating, EventInfoModel.event_time,
                               EventInfoModel.event_image, EventFilerModel.filter) \
            .join(EventFilerModel, EventInfoModel.event_id == EventFilerModel.event_id). \
            filter(EventFilerModel.filter == condition).all()
    else:
        search_str = "%{}%".format(search_val)
        # print(search_str)
        res = db.session.query(EventInfoModel.event_id, EventInfoModel.event_name,
                               EventInfoModel.event_description, EventInfoModel.club_id,
                               EventInfoModel.average_rating, EventInfoModel.event_time,
                               EventInfoModel.event_image, EventFilerModel.filter) \
            .join(EventFilerModel, EventInfoModel.event_id == EventFilerModel.event_id). \
            filter(EventFilerModel.filter == condition).filter(
                EventInfoModel.event_name.like(search_str)).all()

    result = []
    for i in res:
        event_dict = {"event_id": i.event_id,
                      "event_name": i.event_name,
                      "description": i.event_description,
                      "average_rating": i.average_rating,
                      "event_time": i.event_time,
                      "filter": i.filter,
                      "event_image": i.event_image
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
    from backend.models.event_info_model import EventInfoModel  # noqa
    from backend import db
    from backend.logs.admin import setup_logger

    new_event_info = EventInfoModel(event_id, name, desc, organizer)
    try:
        db.session.add(new_event_info)
        db.session.commit()
    except Exception as e:
        operation_log = setup_logger('main_sys.insert_new_events')
        operation_log.error('%s', e)
        return False, str(e)

    return True, ""


@main_sys.route('/view_events')
def view_event():
    data = view_event_impl()
    return jsonify({"code": 200, "msg": "OK", "data": data}), 200


def view_event_impl():
    sql = text("select * from event_info_table;")
    from backend.models.event_info_model import EventInfoModel  # noqa
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
    from models.event_filter_model import EventFilerModel  # noqa
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
    from backend.logs.admin import setup_logger
    new_event_filter = EventFilerModel(event_id, filter_name)
    try:
        db.session.add(new_event_filter)
        db.session.commit()
    except Exception as e:
        operation_log = setup_logger('main_sys.insert_event_impl')
        operation_log.error('%s', e)
        return False, str(e)

    return True, ""


# Add (Post) events
# Create a Posts Form
@main_sys.errorhandler(Exception)
def handle_error(error):
    status_code = 500  # Default status code for Internal Server Error
    message = str(error)
    # Check if the exception has a status_code attribute
    if hasattr(error, 'status_code'):
        status_code = error.status_code
    type = error.__class__.__name__,
    return type, status_code


@main_sys.route('/view/club')
def view_club():
    sql = text("select * from club_info_table;")
    from backend.models.event_info_model import ClubInfoModel
    res = ClubInfoModel.query.from_statement(sql).all()
    result = []
    for i in res:
        event_dict = {"club_id": i.club_id,
                      "club_name": i.club_name,
                      "host_name": i.host_name,
                      "description": i.description,
                      }
        result.append(event_dict)
    return jsonify({"code": 200, "msg": "OK", "data": result}), 200


@main_sys.route('/add/club', methods=['POST'])
@requires_auth
def add_club():
    from backend.models.user_model import UserModel
    from backend.logs.admin import setup_logger
    user = UserModel.query.filter_by(
        user_id=g.current_user["user_id"]).first()
    if user.organizational_role:
        try:
            from backend.models.event_info_model import ClubInfoModel
            club_name_on_form = request.json["club_name"]
            description_on_form = request.json["description"]
            new_club = ClubInfoModel(
                club_name=club_name_on_form,
                description=description_on_form,
                host_name=user.username,
            )
            from backend import db  # noqa
            db.session.add(new_club)
            db.session.commit()
            return jsonify({"code": 200, "msg": "Congrats, you successfully add the club."}), 200
        except Exception as e:
            operation_log = setup_logger('main_sys.add_club')
            operation_log.error('%s', e)
            response, status_code = handle_error(e)
            return jsonify({"code": status_code, "error": response}), status_code
    else:
        return jsonify({"code": 409, "error": "You don't have access to post club as you are not a host."}), 409


@main_sys.route('/view/event')
def view_events():
    from backend.logs.admin import setup_logger
    try:
        sql = text("select * from event_info_table;")
        from backend.models.event_info_model import EventInfoModel
        res = EventInfoModel.query.from_statement(sql).all()
        result = []
        for i in res:
            event_dict = {
                "event_id": i.event_id,
                "event_name": i.event_name,
                "club_id": i.club_id,
                "event_time": i.event_time.strftime('%Y-%m-%d %H:%M:%S'),
                "event_description": i.event_description,
                "address": i.address,
                "fee": i.charge,
                "shared_title": i.shared_title,
            }
            result.append(event_dict)
        response = {
            "code": 200,
            "msg": "OK",
            "data": result
        }
        operation_log = setup_logger('main_sys.view_events_1')
        operation_log.info('this is good')
        return jsonify(response), 200
    except Exception as e:
        operation_log = setup_logger('main_sys.view_events')
        operation_log.error('%s', e)
        print(str(e))  # Print the error for debugging purposes
        return jsonify({"code": 500, "error": "Internal Server Error"}), 500


# Get the parent directory of the current directory
parent_directory = Path(__file__).resolve().parent.parent
# Define the subdirectory for upload images
UPLOAD_FOLDER = os.path.join(parent_directory, 'upload_images')
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])


def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main_sys.route('/host/view')
def view_host_table():
    sql = text("select * from host_event_table;")
    from backend.models.host_event_model import HostEventModel
    res = HostEventModel.query.from_statement(sql).all()
    result = []
    for i in res:
        event_dict = {"host_id": i.host_id,
                      "event_id": i.event_id,
                      }
        result.append(event_dict)
    return jsonify({"code": 200, "msg": "OK", "data": result}), 200


@main_sys.route('/allClubs', methods=['GET'])
def get_club_names():
    from backend.models.event_info_model import ClubInfoModel
    all_club_names = [club.club_name for club in ClubInfoModel.query.all()]
    return jsonify(all_club_names)


@main_sys.route('/add/event', methods=['POST'])
@requires_auth
def add_event():
    from backend.logs.admin import setup_logger

    try:
        from backend.models.user_model import UserModel
        user = UserModel.query.filter_by(
            user_id=g.current_user["user_id"]).first()
        if not user.organizational_role:
            return jsonify({"code": 400, "error": "Sorry, you don't have the access to post event."}), 400

        shared_title_on_form = request.form.get('shared_title')
        file = request.files.getlist('file')
        disallowed_files = []

        for f in file:
            filename = secure_filename(f.filename)
            if allowedFile(filename):
                f.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                disallowed_files.append(filename)

        # Continue processing other form fields
        event_name_on_form = request.form.get("event_name")
        event_time_str = request.form.get("event_time")
        event_time_obj = None
        try:
            event_time_obj = datetime.strptime(
                event_time_str, '%m/%d/%Y %H:%M')
        except ValueError:
            return jsonify({"code": 400,
                            "error": f"Invalid event_time format. Please use the format MM/DD/YYYY HH: MM, e.g., 01/23/2023 14: 30."
                            }), 400
        event_description_on_form = request.form.get("event_description")
        address_on_form = request.form.get("address")
        fee_on_form = request.form.get("fee")
        selected_club_name = request.form.get("club_name")

        from backend.models.event_info_model import ClubInfoModel
        selected_club = ClubInfoModel.query.filter_by(
            club_name=selected_club_name).first()
        # Check if the club exists
        if not selected_club:
            return jsonify({"code": 404, "error": "Club not found."}), 404

        # check if the specific events has been registered before,
        # if registered, return error
        try:
            from backend.models.event_info_model import EventInfoModel
            new_event = EventInfoModel(
                event_name=event_name_on_form,
                event_time=event_time_obj,
                event_description=event_description_on_form,
                address=address_on_form,
                charge=fee_on_form,
                shared_title=shared_title_on_form,
                club_id=selected_club.club_id
            )
            events = EventInfoModel.query.all()
            duplicate_events = False
            for event in events:
                if event == new_event:
                    duplicate_events = True
            if duplicate_events:
                return jsonify({"code": 409, "error": "Event already exists."}), 409

            from backend import db  # noqa
            db.session.add(new_event)
            db.session.commit()
            from backend.models.host_event_model import HostEventModel
            # add the records to host_event_table
            new_host = HostEventModel(
                host_id=user.user_id,
                event_id=new_event.event_id
            )
            db.session.add(new_host)
            db.session.commit()

            # Check if there are disallowed files
            if disallowed_files:
                return jsonify({'error': f'Some files were not processed: {", ".join(disallowed_files)}'}), 200
            else:
                return jsonify({"code": 200, "msg": "Event created successfully."}), 200
        except Exception as e:
            operation_log = setup_logger('main_sys.add_event_1')
            operation_log.error('%s', e)
            response, status_code = handle_error(e)
            return jsonify({"code": status_code, "error": response}), status_code
    except Exception as e:
        operation_log = setup_logger('main_sys.add_event_2')
        operation_log.error('%s', e)
        response, status_code = handle_error(e)
        return jsonify({"code": status_code, "error": response}), status_code
