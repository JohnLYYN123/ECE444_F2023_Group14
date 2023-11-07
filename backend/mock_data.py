from backend.models.event_info_model import EventInfoModel  # noqa
from models.event_info_model_mock_data import event_info_model_mock_data


def event_info_mocking(db):
    mock_data = event_info_model_mock_data[0]
    event_info_instance = EventInfoModel(
        mock_data["event_name"],
        mock_data["event_time"],
        mock_data["number_rater"],
        mock_data["average_rating"],
        mock_data["event_description"],
        mock_data["club_id"]
    )
    print(event_info_instance)
    db.session.add(event_info_instance)
    db.session.commit()
