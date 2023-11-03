from backend import app, db
from models.user_model import UserModel
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
