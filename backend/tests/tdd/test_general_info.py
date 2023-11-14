from backend import app
import pytest
from test_general_info_mock import mock_all_event, mock_event_2

header = {"Authorization": 'eyJ1c2VyX2lkIjoxLCJ1b2Z0X2VtYWlsIjoiZ3VpdGFyLmhlcm9AbWFpbC51dG9yb250by5jYSJ9.ZVEhJw.L8uu9748wABRiu7cpVo4U45Uzyg'}


def test_without_authentication():
    client = app.test_client()
    res = client.get('/main_sys/?event_id=-1')
    assert res.status_code == 401
    assert res.json == {"code": 401, "error": "Authentication is required to access this resource"}


def test_with_authentication():
    client = app.test_client()
    res = client.get('/main_sys/?event_id=', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "Event id is empty", "data": []}


def test_specific_event():
    test_data = mock_event_2
    client = app.test_client()
    res = client.get('/main_sys/?event_id=2', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "success", "data": test_data}


def test_all_event():
    test_data = mock_all_event
    client = app.test_client()
    res = client.get('/main_sys/?event_id=-1', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "success", "data": test_data}


def test_empty_event():
    client = app.test_client()
    res = client.get('/main_sys/?event_id=20', headers=header)
    assert res.status_code == 401
    assert res.json == {"code": 401, "msg": "Event does not exist", "data": []}
