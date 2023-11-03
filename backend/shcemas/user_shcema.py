from backend import app, db
from models.user import User
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
