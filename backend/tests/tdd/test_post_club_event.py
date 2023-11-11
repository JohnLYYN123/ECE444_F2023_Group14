import pytest
from backend import app, db, bcrypt


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()


def test_unauthorized_access_post_club(client):
    data = {
        'club_name': 'TestClub',
        'description': 'This is a test club.'
    }

    with client:
        response = client.post('main_sys/add/club', json=data)
        assert response.status_code == 401
        assert 'Authentication is required to access this resource' in response.json[
            'message']


def test_register_accepts_post_only(client):
    response = client.get('main_sys/add/event')
    assert response.status_code == 405
    allowed_methods = response.headers.get('Allow', '').split(', ')
    assert 'POST' in allowed_methods
