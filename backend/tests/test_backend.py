from backend import app
import pytest


@pytest.fixture
# Yun Ru test login for Lab 5
def test_valid_login():
    client = app.test_client()
    response = client.post(
        '/user/login', json={'username': 'user', 'password': 'password'})
    assert response.status_code == 200
    assert response.json == {'message': 'Login successful'}

# Yun Ru test login for Lab 5


def test_empty_credentials():
    client = app.test_client()
    response = client.post(
        '/user/login', json={'username': '', 'password': ''})
    assert response.status_code == 409
    assert response.json == {"error": "Unauthorized Access"}

# Eric Zheng testing add comment for Lab 5


def test_new_comment_success():
    client = app.test_client()
    response = client.post(
        '/detail/add', json={'Title': 'testing', 'Content': 'testing'})
    assert response.status_code == 302  # should get redirected temporarily

# Eric Zheng testing add empty comment for Lab 5


def test_new_comment_fail():
    client = app.test_client()
    response = client.post('/detail/add', json={'Title': '', 'Content': ''})
    assert response.status_code == 406  # should be not acceptable
