from backend.app import create_app
import pytest

@pytest.fixture

def app():
    app = create_app()
    return app

# Yun Ru test login for Lab 5
def test_valid_login(app):
    client = app.test_client()
    response = client.post('/user/login', json={'username': 'user', 'password': 'password'})
    assert response.status_code == 200
    assert response.json == {'message': 'Login successful'}

# Yun Ru test login for Lab 5
def test_empty_credentials(app):
    client = app.test_client()
    response = client.post('/user/login', json={'username': '', 'password': ''})
    assert response.status_code == 401
    assert response.json == {'message': 'One of the entries is empty'}

    