from flask import Blueprint, jsonify, render_template, request
user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'One of the entries is empty'}), 401
    else:
        return jsonify({'message': 'Login successful'}), 200


@user.route("register", methods=['POST'])
def register():
    from models.user import User  # noqa
    from backend import db
    new_user = User('z', 'x', 'sd')
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return False, str(e)

    return True, ""
