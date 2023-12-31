from datetime import datetime
from sqlalchemy import CheckConstraint, ForeignKey
from backend import db


# for review_user attribute, we may need another foreign key constraint
class ReviewRatingModel(db.Model):
    __tablename__ = "review_rating_table"
    __table_args__ = {'extend_existing': True}
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, ForeignKey('event_info_table.event_id', ondelete="CASCADE"))
    review_user = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, CheckConstraint('rating >= 0 and rating <= 5', name='rating_check'), default=0)
    review_comment = db.Column(db.Text)
    review_time = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, review_dict):
        self.event_id = review_dict["event_id"]
        self.review_user = review_dict["review_user"]
        self.rating = review_dict["rating"]
        self.review_comment = review_dict["review_comment"]



