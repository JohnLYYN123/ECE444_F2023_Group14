from backend import app
import pytest


header = {"Authorization": 'eyJ1c2VyX2lkIjoxLCJ1b2Z0X2VtYWlsIjoiZ3VpdGFyLmhlcm9AbWFpbC51dG9yb250by5jYSJ9.ZVEhJw.L8uu9748wABRiu7cpVo4U45Uzyg'}

def test_without_header():
    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=1')
    assert res.status_code == 401
    assert res.json == {"code": 401, "error": "Authentication is required to access this resource"}


def test_empty_event_id():
    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=', headers=header)
    print(res)
    assert res.status_code == 401
    assert res.json == {"code": 401, "msg": "empty input date when should not be empty",
                        "data": []}


def test_negative_event_id():
    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=-1', headers=header)
    assert res.status_code == 401
    assert res.json == {"code": 401, "msg": "Negative event_id is not allowed",
                        "data": []}


def test_not_existing_event_id():
    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=100', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "event does not exist", "data": []}


def test_event_id_equal_2():
    test_data = {
        "event_info": {
            "address": "777 Bay ST.",
            "average_rating": 4.0,
            "charge": 0.0,
            "club_desc": "represent engineering students in basketball team",
            "club_id": 2,
            "club_name": "Skule basketball team",
            "event_description": "help student with ECE444 project and have a secret party",
            "event_id": 2,
            "event_image": "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png",
            "event_name": "Basketball Tryout",
            "event_time": "Fri, 03 Nov 2023 14:00:00 GMT",
            "host_name": "John",
            "number_rater": 2,
            "position_address": "Exam Center"
        },
        "review_info": {
            "avg_rating": 4.0,
            "number_review": 2,
            "review_detail": [
                {
                    "rating": 5,
                    "review_comment": "Good spirit and so much fun",
                    "review_time": "Mon, 13 Nov 2023 20:34:50 GMT",
                    "review_user": "guitar"
                },
                {
                    "rating": 3,
                    "review_comment": "FUN FUN FUN",
                    "review_time": "Mon, 13 Nov 2023 20:34:50 GMT",
                    "review_user": "sam"
                }
            ]
        }
    }

    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=2', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "OK", "data": test_data}


