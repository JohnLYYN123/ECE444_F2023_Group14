import pytest
from backend import app, db, bcrypt


def test_register_accepts_post_only():
    client = app.test_client()
    response = client.get('main_sys/add/event')
    assert response.status_code == 405
    allowed_methods = response.headers.get('Allow', '').split(', ')
    assert 'POST' in allowed_methods
