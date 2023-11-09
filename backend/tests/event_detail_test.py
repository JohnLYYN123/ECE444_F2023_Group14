from backend import app
import pytest


@pytest.fixture
def test_empty_event_id():
    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=')
    assert res.status_code == 401
    assert res.json == {"code": 401, "msg": "empty input date when should not be empty",
                        "data": []}


def test_negative_event_id():
    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=-1')
    assert res.status_code == 401
    assert res.json == {"code": 401, "msg": "Negative event_id is not allowed",
                        "data": []}


def test_not_existing_event_id():
    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=100')
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "event does not exist", "data": []}


def test_event_id_equal_2():
    test_data = {
        "event_info": {
            "address": None,
            "average_rating": 4,
            "charge": 0,
            "club_desc": "the clubs is fun and party all day",
            "club_id": 1,
            "club_name": "Jerry clubs",
            "event_description": "help student with ECE444 project and have a secret party",
            "event_id": 2,
            "event_image": "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png",
            "event_name": "Basketball Tryout",
            "event_time": "Fri, 03 Nov 2023 14:00:00 GMT",
            "host_name": "Jerry",
            "number_rater": 2,
            "position_address": None
        },
        "review_info": {
            "avg_rating": 4,
            "number_review": 2,
            "review_detail": [
                {
                    "rating": 5,
                    "review_comment": "Good spirit and so much fun",
                    "review_time": "Wed, 08 Nov 2023 11:00:00 GMT",
                    "review_user": "guitar"
                },
                {
                    "rating": 3,
                    "review_comment": "FUN FUN FUN",
                    "review_time": "Wed, 08 Nov 2023 11:00:00 GMT",
                    "review_user": "sam"
                }
            ]
        }
    }

    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=2')
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "OK", "data": test_data}

