from sqlalchemy import text
from ..Database import Event_DB
class MainSysModel:
    def filter_event(self, filter_list):
        condition = filter_list
        sql = text("select * from event_filter_db where filter = :cond")
        res = Event_DB.EventFilerDB.query.from_statement(sql.bindparams(cond=condition)).all()
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
        sql_conn = Event_DB.t_event_filter_db
        new_event_filter = Event_DB.EventFilerDB(event_id, filter_name)
        try:
            sql_conn.session.add(new_event_filter)
            sql_conn.session.commit()
        except Exception as e:
            return False, str(e)

        return True, ""

