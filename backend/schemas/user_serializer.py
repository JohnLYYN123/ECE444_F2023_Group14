from backend import app, db
from flask_marshmallow import Marshmallow
from models import user

ma = Marshmallow(app)


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = user
