from backend import app
import pytest

header_with_events = {"Authorization": 'eyJ1c2VyX2lkIjo0LCJ1b2Z0X2VtYWlsIjoiam9obi5saW5AbWFpbC51dG9yb250by5jYSJ9.ZVAkHw.GVCf4O4Jt96wvYg8eAzSL5OE0U4'}
header_no_event = {"Authorization": 'eyJ1c2VyX2lkIjo1LCJ1b2Z0X2VtYWlsIjoiZC5kQG1haWwudXRvcm9udG8uY2EifQ.ZVDq3Q.yeD4R3npwWE6jA2LzHz66Tfo-2Q'}

def test_without_header():
    client = app.test_client()
    res = client.get('http://127.0.0.1:5000/enroll/')
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
            "event_id": 3,
            "event_image": "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png",
            "event_name": "ECE444 project help session 2",
            "event_time": "Sat, 04 Nov 2023 14:00:00 GMT",
            "filter_info": [
                "art",
                "sport"
            ]
        }
    ]
    client = app.test_client()
    res = client.get('http://127.0.0.1:5000/enroll/', headers=header_with_events)
    assert res.status_code == 200
    assert res.json == {"code": 200, "future": future_events, "past": past_event}


def test_no_event():
    client = app.test_client()
    res = client.get('http://127.0.0.1:5000/enroll/', headers=header_no_event)
    assert res.status_code == 404
    assert res.json == {"code": 404, "error": "No enrolled events for the user"}
