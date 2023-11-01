from backend import app
import pytest


@pytest.fixture
def test_empty_input():
    client = app.test_client()
    res = client.get('/main_sys/filter?title=')
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "No filter applied", "data": []}


def test_invalid_title():
    client = app.test_client()
    res = client.get('/main_sys/filter?title=SPORTS')
    assert res.status_code == 200
    assert res.json == {"code": 200,
                        "msg": "filter does not exist", "data": []}
