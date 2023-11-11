import pytest
from backend import app, db, bcrypt
from backend.models.user_model import UserModel


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()


def test_register_existing_user(client):
    # Create a user before testing registration of an existing user
    existing_user = UserModel(
        username='existinguser',
        uoft_email='existinguser@utoronto.ca',
        password_hash=bcrypt.generate_password_hash(
            'existingpassword').decode('utf-8'),
        uoft_student_id='54321',
        first_name='Existing',
        last_name='User',
        department='Example Department',
        enrolled_time='2023-11-10',
        organizational_role=False
    )
    with app.app_context():
        db.session.add(existing_user)
        db.session.commit()

    data = {
        'username': 'existinguser',
        'uoftEmail': 'existinguser@utoronto.ca',
        'password': 'existingpassword',
        'uoftStudentId': '54321',
        'firstName': 'Existing',
        'lastName': 'User',
        'enrolledTime': '2023-11-10',
        'organizationalRole': False
    }

    response = client.post('/user/register', json=data)

    assert response.status_code == 401
    assert 'Username already exists' in response.json['error']


def test_login_successful(client):
    # Create a user before testing login
    user = UserModel(
        username='testuser',
        uoft_email='testuser@utoronto.ca',
        password_hash=bcrypt.generate_password_hash(
            'testpassword').decode('utf-8'),
        uoft_student_id='12345',
        first_name='Test',
        last_name='User',
        department='Example Department',
        enrolled_time='2023-11-10',
        organizational_role=False
    )
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    data = {
        'username': 'testuser',
        'password': 'testpassword'
    }

    response = client.post('/user/login', json=data)

    assert response.status_code == 200
    assert 'token' in response.json


def test_login_wrong_password(client):
    # Create a user before testing login
    user = UserModel(
        username='testuser',
        uoft_email='testuser@utoronto.ca',
        password_hash=bcrypt.generate_password_hash(
            'testpassword').decode('utf-8'),
        uoft_student_id='12345',
        first_name='Test',
        last_name='User',
        department='Example Department',
        enrolled_time='2023-11-10',
        organizational_role=False
    )
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    data = {
        'username': 'testuser',
        'password': 'wrongpassword'
    }

    response = client.post('/user/login', json=data)

    assert response.status_code == 401
    assert 'Wrong Password - Try Again!' in response.json['error']


def test_login_unauthorized_access(client):
    data = {
        'username': 'nonexistentuser',
        'password': 'testpassword'
    }

    response = client.post('/user/login', json=data)

    assert response.status_code == 409
    assert 'Unauthorized Access' in response.json['error']
