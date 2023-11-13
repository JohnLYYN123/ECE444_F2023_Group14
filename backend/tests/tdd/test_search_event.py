from backend import app
import pytest
from test_search_event_mock import multiple_response_mock, single_response_mock, request_with_whitespace_mock

header = {"Authorization": 'eyJ1c2VyX2lkIjoxLCJ1b2Z0X2VtYWlsIjoiZ3VpdGFyLmhlcm9AbWFpbC51dG9yb250by5jYSJ9.ZVEhJw.L8uu9748wABRiu7cpVo4U45Uzyg'}


def test_without_authentication():
    client = app.test_client()
    res = client.get('/main_sys/search?value=ECE444')
    assert res.status_code == 401
    assert res.json == {"code": 401, "error": "Authentication is required to access this resource"}


def test_with_authentication():
    test_data = multiple_response_mock
    client = app.test_client()
    res = client.get('/main_sys/search?value=ECE444', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "success", "data": test_data}


def test_search_with_single_output():
    client = app.test_client()
    res = client.get('/main_sys/search?value=Basketball', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "success", "data": single_response_mock}


def test_with_whitespace():
    client = app.test_client()
    res = client.get('/main_sys/search?value=Basketball Tryout', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "success", "data": request_with_whitespace_mock}


def test_with_no_response():
    client = app.test_client()
    res = client.get('/main_sys/search?value=BasketballTryout', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "success", "data": []}
