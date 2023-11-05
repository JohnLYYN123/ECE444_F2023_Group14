from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import text
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import (DateTimeField, StringField, TextAreaField,
                     ValidationError, SubmitField)
from wtforms.validators import InputRequired, Length, Optional
import json


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
    from models.event_filter_model import EventFilerModel  # noqa
    from models.event_info_model import EventInfoModel  # noqa
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
class PostEventForm(FlaskForm):
    event_name = StringField(validators=[
                             InputRequired(), Length(max=256)])
    event_time = DateTimeField(validators=[InputRequired()])
    event_description = TextAreaField(validators=[InputRequired()])
    position_addre = StringField(validators=[Optional()])
    address = StringField(validators=[Optional()])
    fee = StringField(validators=[Optional()])
    # for poster
    shared_title = StringField(validators=[Optional()])
    shared_image = StringField(validators=[Optional()])
    submit = SubmitField("Post the event")


class PostClubForm(FlaskForm):
    club_name = StringField(validators=[
        InputRequired(), Length(max=256)])
    description = TextAreaField(validators=[InputRequired()])
    submit = SubmitField("Register the club")


@main_sys.errorhandler(Exception)
def handle_error(error):
    status_code = 500  # Default status code for Internal Server Error
    message = str(error)

    # Check if the exception has a status_code attribute
    if hasattr(error, 'status_code'):
        status_code = error.status_code

    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }

    flash(f"Error: {message}", 'error')
    return response, status_code


@main_sys.route('/club/view')
def view_club():
    sql = text("select * from club_info_table;")
    from backend.models.club_info_model import ClubInfoModel
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


@main_sys.route('/add/club', methods=['GET', 'POST'])
@login_required
def add_club():
    form = PostClubForm()
    if form.validate_on_submit():
        if current_user.authenticated and current_user.organizational_role:
            print(request.form)
            try:
                from backend.models.club_info_model import ClubInfoModel
                print(current_user.username)
                club_name_on_form = form.club_name.data
                description_on_form = form.description.data
                new_club = ClubInfoModel(
                    club_name=club_name_on_form,
                    description=description_on_form,
                    host_name=current_user.username,
                )
                print(new_club.club_id)
                from backend import db  # noqa
                db.session.add(new_club)
                db.session.commit()
                flash(f"Club Succesfully created", "success")
                return jsonify({"code": 200, "msg": "Congrats, you successfully add the club."}), 200
            except Exception as e:
                response, status_code = handle_error(e)
                flash(response['error']['message'], 'error')
                return jsonify(response), status_code
        else:
            print("Debug1")
    else:
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append({
                    'field': field,
                    'message': error
                })
        # Flash individual error messages
        for error in error_messages:
            flash(f"Field '{error['field']}': {error['message']}", 'error')
    return render_template('add_club.html', form=form)

    # form = ()
    # if form.validate_on_submit():
    #     try:
    #         from backend.models import ClubInfoModel
    #     except Exception as e:
    #         response, status_code = handle_error(e)
    #         flash(response['error']['message'], 'error')
    #         return jsonify(response), status_code
    # else:
    #         error_messages = []
    #         for field, errors in form.errors.items():
    #             for error in errors:
    #                 error_messages.append({
    #                     'field': field,
    #                     'message': error
    #                 })
    #         # Flash individual error messages
    #         for error in error_messages:
    #             flash(f"Field '{error['field']}': {error['message']}", 'error')


@main_sys.route('/add/event', methods=['GET', 'POST'])
@login_required
def add_event():
    form = PostEventForm()
    if form.validate_on_submit():
        if current_user.authenticated and current_user.organizational_role:
            try:
                from backend.models import EventInfoModel, HostEventModel
                event_name_on_form = form.event_name.data
                event_time_on_form = form.event_time.data
                event_description_on_form = form.event_description.data
                position_addre_on_form = form.position_addre.data
                address_on_form = form.address.data
                fee_on_form = form.fee.data
                share_title_on_form = form.shared_title.data
                shared_image_on_form = form.shared_image.data
                # add the form data into event_info_table
                new_event = EventInfoModel(
                    event_name=event_name_on_form,
                    event_time=event_time_on_form,
                    event_description=event_description_on_form,
                    position_addre=position_addre_on_form,
                    address=address_on_form,
                    charge=fee_on_form,
                    shared_title=share_title_on_form,
                    shared_image=shared_image_on_form,
                )
                # add the records to host_event_table
                new_host = HostEventModel(
                    host_id=current_user.user_id,
                    event_id=new_event.event_id
                )
                flash(f"Account Succesfully created", "success")
                return jsonify({"code": 200, "msg": "Congrats, you successfully post the event."}), 200
            except Exception as e:
                response, status_code = handle_error(e)
                flash(response['error']['message'], 'error')
                return jsonify(response), status_code
        else:
            return jsonify({"code": 400, "msg": "Sorry, you don't have the access to post event."}), 400
    else:
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append({
                    'field': field,
                    'message': error
                })
        # Flash individual error messages
        for error in error_messages:
            flash(f"Field '{error['field']}': {error['message']}", 'error')
