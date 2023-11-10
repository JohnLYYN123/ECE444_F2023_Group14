from models.event_info_model import EventInfoModel
from models.event_info_model_mock_data import event_info_model_mock_data
from models.event_filter_model import EventFilerModel
from models.event_filter_model_mock_data import filter_info_model_mock_data


def event_info_mocking(db):
    mock_data_models = event_info_model_mock_data
    for mock_data in mock_data_models:
        event_info_instance = EventInfoModel(
            mock_data["event_name"],
            mock_data["event_time"],
            mock_data["number_rater"],
            mock_data["event_description"],
            mock_data["event_image"],
            mock_data["club_id"],
            average_rating=mock_data["average_rating"]
        )
        print(event_info_instance)
        db.session.add(event_info_instance)
        db.session.commit()


def filter_info_mocking(db):
    mock_filters = filter_info_model_mock_data
    for mock_filter in mock_filters:
        filter_instance = EventFilerModel(
            mock_filter["event_id"],
            mock_filter["filter"]
        )
        print(filter_instance)
        db.session.add(filter_instance)
        db.session.commit()
