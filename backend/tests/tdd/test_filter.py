from backend import app
import pytest


@pytest.fixture
def test_empty_input():
    client = app.test_client()
    res = client.get('/main_sys/filter?title=')
    assert res.status_code == 401
    assert res.json == {"code": 401, "msg": "No filter applied", "data": []}


def test_invalid_title():
    client = app.test_client()
    res = client.get('/main_sys/filter?title=SPORTS')
    assert res.status_code == 401
    assert res.json == {"code": 401,
                        "msg": "filter does not exist", "data": []}


def test_not_exist_title():
    client = app.test_client()
    res = client.get('/main_sys/filter?title=study')
    assert res.status_code == 401
    assert res.json == {"code": 401,
                        "msg": "filter does not exist", "data": []}


def test_valid_filter():
    client = app.test_client()
    res = client.get('/main_sys/filter?title=art')

    test_data = [
        {
            "average_rating": 3.5,
            "description": "help student with ECE444 project and have a secret party",
            "event_id": 2,
            "event_image": "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png",
            "event_name": "Basketball Tryout",
            "event_time": "Fri, 03 Nov 2023 14:00:00 GMT",
            "filter": "art"
        },
        {
            "average_rating": 3.5,
            "description": "help student with ECE444 project and have a secret party",
            "event_id": 3,
            "event_image": "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png",
            "event_name": "ECE444 project help session 2",
            "event_time": "Sat, 04 Nov 2023 14:00:00 GMT",
            "filter": "art"
        }
    ]

    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "OK", "data": test_data}


def test_valid_filter_empty_search_value():
    test_data = [
        {
            "average_rating": 3.5,
            "description": "help student with ECE444 project and have a secret party",
            "event_id": 2,
            "event_image": "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png",
            "event_name": "Basketball Tryout",
            "event_time": "Fri, 03 Nov 2023 14:00:00 GMT",
            "filter": "art"
        },
        {
            "average_rating": 3.5,
            "description": "help student with ECE444 project and have a secret party",
            "event_id": 3,
            "event_image": "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png",
            "event_name": "ECE444 project help session 2",
            "event_time": "Sat, 04 Nov 2023 14:00:00 GMT",
            "filter": "art"
        }
    ]

    client = app.test_client()
    res = client.get('/main_sys/filter?title=art&search_value=')
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "OK", "data": test_data}

def test_valid_filter_valid_search_value():
    test_data = [
        {
            "average_rating": 3.5,
            "description": "help student with ECE444 project and have a secret party",
            "event_id": 2,
            "event_image": "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png",
            "event_name": "Basketball Tryout",
            "event_time": "Fri, 03 Nov 2023 14:00:00 GMT",
            "filter": "art"
        }
    ]

    client = app.test_client()
    res = client.get('/main_sys/filter?title=art&search_value=basketball')
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "OK", "data": test_data}


def test_valid_filter_valid_search_value_2():
    client = app.test_client()
    res = client.get('/main_sys/filter?title=art&search_value=random')
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "OK", "data": []}


