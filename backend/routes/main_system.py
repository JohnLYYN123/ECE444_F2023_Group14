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


def get_event_info(event_id):
    from backend.models.event_info_model import EventInfoModel  # noqa
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
    from models.event_filter_model import EventFilerModel  # noqa
    from backend.models.event_info_model import EventInfoModel  # noqa
    from backend import db  # noqa
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
    from backend.models.event_info_model import EventInfoModel  # noqa
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
    new_event_filter = EventFilerModel(event_id, filter_name)
    try:
        db.session.add(new_event_filter)
        db.session.commit()
    except Exception as e:
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
            response, status_code = handle_error(e)
            return jsonify({"code": status_code, "error": response}), status_code
    else:
        return jsonify({"code": 409, "error": "You don't have access to post club as you are not a host."}), 409


@main_sys.route('/view/event')
def view_events():
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
        return jsonify(response), 200
    except Exception as e:
        print(str(e))  # Print the error for debugging purposes
        return jsonify({"code": 500, "error": "Internal Server Error"}), 500


# Get the parent directory of the current directory
parent_directory = Path(__file__).resolve().parent.parent
# Define the subdirectory for upload images
UPLOAD_FOLDER = os.path.join(parent_directory, 'upload_images')
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif',])


def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main_sys.route('/upload', methods=['POST'])
# @requires_auth
def fileUpload():
    # upload image to share here
    if request.method == 'POST':
        try:
            shared_title = request.form.get('shared_title')
            file = request.files.getlist('file')
            for f in file:
                filename = secure_filename(f.filename)
                if allowedFile(filename):
                    f.save(os.path.join(UPLOAD_FOLDER, filename))
                else:
                    return jsonify({'message': 'File type not allowed'}), 400
            return jsonify({"code": 200, "msg": "upload photo successfully."}), 200
        except Exception as e:
            response, status_code = handle_error(e)
            return jsonify({"code": status_code, "error": response}), status_code


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
    try:
        from backend.models.user_model import UserModel
        user = UserModel.query.filter_by(
            user_id=g.current_user["user_id"]).first()
        if not user.organizational_role:
            return jsonify({"code": 400, "msg": "Sorry, you don't have the access to post event."}), 400

        event_name_on_form = request.json["event_name"]
        event_time_str = request.json["event_time"]
        event_time_obj = None
        try:
            event_time_obj = datetime.strptime(
                event_time_str, '%m/%d/%Y %H:%M')
        except ValueError:
            return jsonify({"code": 400,
                            "error": f"Invalid event_time format. Please use the format MM/DD/YYYY HH: MM, e.g., 01/23/2023 14: 30."
                            }), 400
        event_description_on_form = request.json["event_description"]
        address_on_form = request.json["address"]
        fee_on_form = request.json["fee"]
        # share_title_on_form = request.json["shared_title"]

        selected_club_name = request.json["club_name"]
        from backend.models.event_info_model import ClubInfoModel
        selected_club = ClubInfoModel.query.filter_by(
            club_name=selected_club_name).first()
        # Check if the club exists
        if not selected_club:
            return jsonify({"code": 404, "error": "Club not found."}), 404

        # check if the specific events has been registerd before,
        # if registered, return error
        try:
            from backend.models.event_info_model import EventInfoModel
            new_event = EventInfoModel(
                event_name=event_name_on_form,
                event_time=event_time_obj,
                event_description=event_description_on_form,
                address=address_on_form,
                charge=fee_on_form,
                # shared_title=share_title_on_form,
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
            return jsonify({"code": 200, "msg": "Event created successfully."}), 200
        except Exception as e:
            response, status_code = handle_error(e)
            return jsonify({"code": status_code, "error": response}), status_code
    except Exception as e:
        response, status_code = handle_error(e)
        return jsonify({"code": status_code, "error": response}), status_code
