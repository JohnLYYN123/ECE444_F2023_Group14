from backend import app
import pytest

header_with_events = {"Authorization": 'eyJ1c2VyX2lkIjoxLCJ1b2Z0X2VtYWlsIjoiZ3VpdGFyLmhlcm9AbWFpbC51dG9yb250by5jYSJ9.ZVEhJw.L8uu9748wABRiu7cpVo4U45Uzyg'}
header_no_event = {"Authorization": 'eyJ1c2VyX2lkIjoyLCJ1b2Z0X2VtYWlsIjoic2FtLm1hc0BtYWlsLnV0b3JvbnRvLmNhIn0.ZVEh1Q.Tyf79Asb3fpwMAu8p2FZ2kXRB0k'}

def test_without_header():
    client = app.test_client()
    res = client.get('/enroll/')
    assert res.status_code == 401
    assert res.json == {"code": 401, "error": "Authentication is required to access this resource"}


def test_header_with_event():
    future_events = [
        {
            "average_rating": 3.5,
            "event_address": "777 Bay ST.",
            "event_id": 1,
            "event_image": "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png",
            "event_name": "ECE444 project help session",
            "event_time": "Mon, 04 Nov 2024 14:00:00 GMT",
            "filter_info": [
                "cooking",
                "sport",
                "travel"
            ]
        }
    ]

    past_event = [
        {
            "average_rating": 3.5,
            "event_address": "777 Bay ST.",
            "event_id": 2,
            "event_image": "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png",
            "event_name": "Basketball Tryout",
            "event_time": "Fri, 03 Nov 2023 14:00:00 GMT",
            "filter_info": [
                "art"
            ]
        }
    ]
    client = app.test_client()
    res = client.get('/enroll/', headers=header_with_events)
    assert res.status_code == 200
    assert res.json == {"code": 200, "future": future_events, "past": past_event}


def test_no_event():
    client = app.test_client()
    res = client.get('/enroll/', headers=header_no_event)
    assert res.status_code == 404
    assert res.json == {"code": 404, "error": "No enrolled events for the user"}
