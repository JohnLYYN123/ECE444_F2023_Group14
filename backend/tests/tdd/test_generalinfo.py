from backend import app
import pytest

@pytest.fixture
def test_empty_input():
    client = app.test_client()
    res = client.get('/main_sys/event_id=')
    assert res.status_code == 401

def test_specific_event():
    test_data = [
        {
            "event_id": 2,
            "event_name": "Basketball Tryout",
            "event_time": "Fri, 03 Nov 2023 14:00:00 GMT",
            "average_rating": 3.5
            
        }
    ]
    client = app.test_client()
    res = client.get('/main_sys/event_id=2')
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "OK", "data": test_data}

def test_all_event():
    test_data = [
        {
            "event_id": 2,
            "event_name": "Basketball Tryout",
            "event_time": "Fri, 03 Nov 2023 14:00:00 GMT",
            "average_rating": 3.5
        },
        {
            "event_id": 3,
            "event_name": "ECE444 project help session 2",
            "event_time": "Sat, 04 Nov 2023 14:00:00 GMT",
            "average_rating": 3.5
        }
    ]
    client = app.test_client()
    res = client.get('/main_sys/event_id=-1')
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "OK", "data": test_data}
