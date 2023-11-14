import pytest
from backend import app, bcrypt
from backend.models.user_model import UserModel


def test_register_existing_user():
    client = app.test_client()
    data = {
        "username": "guitar hero",
        "uoftEmail": "guitar.hero@mail.utoronto.ca",
        "uoftStudentId": "1004140140",
        "firstName": "guitar",
        "lastName": "hero",
        "department": "Music",
        "enrolled_time": "2023",
        "password": bcrypt.generate_password_hash("asdf").decode('utf-8'),
        "organizational_role": True
    }

    response = client.post('/user/register', json=data)
    assert 'Username already exists' in response.json['error']


def test_login_successful():
    client = app.test_client()
    data = {
        'username': 'guitar hero',
        'password': 'asdf'
    }

    response = client.post('/user/login', json=data)

    assert response.status_code == 200
    assert 'token' in response.json


def test_login_wrong_password():
    client = app.test_client()
    data = {
        'username': 'guitar hero',
        'password': 'wrongpassword'
    }
    response = client.post('/user/login', json=data)
    assert response.status_code == 401
    assert 'Wrong Password - Try Again!' in response.json['error']


def test_login_unauthorized_access():
    client = app.test_client()
    data = {
        'username': 'nonexistentuser',
        'password': 'testpassword'
    }
    response = client.post('/user/login', json=data)
    assert response.status_code == 409
    assert 'Please register an account first!' in response.json['error']
