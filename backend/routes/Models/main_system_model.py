from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy import text
from datetime import datetime
from pprint import pprint


t_event_filter_db = SQLAlchemy()


class EventFilerDB(t_event_filter_db.Model):
    __tablename__ = "event_filter_db"
    event_id = t_event_filter_db.Column(t_event_filter_db.Integer, primary_key=True)
    filter = t_event_filter_db.Column(t_event_filter_db.String(256), primary_key=True)
    create_time = t_event_filter_db.Column(t_event_filter_db.DateTime, default=datetime.utcnow())
    update_time = t_event_filter_db.Column(t_event_filter_db.DateTime, onupdate=datetime.utcnow())

    filter_check = CheckConstraint("filter IN ('sport', 'art', 'travel', 'cooking')", name="filter_check_constraint")

    def __init__(self, event_id, filter_name):
        self.event_id = event_id
        self.filter = filter_name

class MainSysModel:
    def filter_event(self, filter_list):
        condition = filter_list
        sql = text("select * from event_filter_db where filter = :cond")
        res = EventFilerDB.query.from_statement(sql.bindparams(cond=condition)).all()
        result = []
        temp_dict = {"event1": "Basketball Tryout",
                     "event2": "Cooking 101",
                     "event3": "Cook and Game",
                     "event4": "Hiking and Biking"}
        for i in res:
            key = "event"+str(i.event_id)
            event_name = temp_dict[key]
            event_dict = {"event_id": i.event_id,
                          "event_name": event_name,
                          "filter_type": i.filter}
            result.append(event_dict)
        return result

    def insert_event(self, event_id, filter_name):
        new_event_filter = EventFilerDB(event_id, filter_name)
        try:
            t_event_filter_db.session.add(new_event_filter)
            t_event_filter_db.session.commit()
        except Exception as e:
            return False, str(e)

        return True, ""

