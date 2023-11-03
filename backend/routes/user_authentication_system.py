from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from schemas.user_serializer import UserSchema
from backend import login_manager
from flask_login import LoginManager
from backend import app
from form.user_form import register_form, login_form

# initialize login_namager
login_manager = LoginManager()
login_manager.init_app(app)
user = Blueprint("user", __name__, url_prefix="/user")


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param integer user_id: user to retrieve

    """
    from models.user import User  # noqa
    return User.query.get(int(user_id))


@user.route("register", methods=['POST', 'GET'])
# @login_required
def register():
    form = register_form()
    # if form.validate_on_submit() and request.method == 'POST':
    #     try:
    #         email = form.email.data
    #         pwd = form.pwd.data
    #         username = form.username.data

    #         newuser = User(
    #             username=username,
    #             email=email,
    #             pwd=bcrypt.generate_password_hash(pwd),
    #         )

    #         db.session.add(newuser)
    #         db.session.commit()
    #         flash(f"Account Succesfully created", "success")
    #         return redirect(url_for("login"))

    #     except Exception as e:
    #         flash(e, "danger")


@user.route("/login", methods=['POST'])
def login():
    form = login_form()
    if form.validate_on_submit():

#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({'message': 'One of the entries is empty'}), 401
#     else:
#         return jsonify({'message': 'Login successful'}), 200
