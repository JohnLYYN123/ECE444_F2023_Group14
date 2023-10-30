from backend.app import create_app
import pytest

@pytest.fixture

def app():
    app = create_app()
    return app

def test_empty_input(app):
    client = app.test_client()
    res = client.get('/main_sys/filter?title=')
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "No filter applied", "data": []}

def test_invalid_title(app):
    client = app.test_client()
    res = client.get('/main_sys/filter?title=SPORTS')
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "filter does not exist", "data": []}

