from backend import app
import pytest


header = {"Authorization": 'eyJ1c2VyX2lkIjo0LCJ1b2Z0X2VtYWlsIjoiam9obi5saW5AbWFpbC51dG9yb250by5jYSJ9.ZVAkHw.GVCf4O4Jt96wvYg8eAzSL5OE0U4'}

def test_without_header():
    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=1')
    assert res.status_code == 401
    assert res.json == {"code": 401, "error": "Authentication is required to access this resource"}


def test_empty_event_id():
    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=', headers=header)
    print(res)
    assert res.status_code == 401
    assert res.json == {"code": 401, "msg": "empty input date when should not be empty",
                        "data": []}


def test_negative_event_id():
    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=-1', headers=header)
    assert res.status_code == 401
    assert res.json == {"code": 401, "msg": "Negative event_id is not allowed",
                        "data": []}


def test_not_existing_event_id():
    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=100', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "event does not exist", "data": []}


def test_event_id_equal_2():
    test_data = {"event_info": {
            "address": "777 Bay ST.",
            "average_rating": 4.0,
            "charge": 0.0,
            "club_desc": "represent engineering students in basketball team",
            "club_id": 2,
            "club_name": "Skule basketball team",
            "event_description": "help student with ECE444 project and have a secret party",
            "event_id": 2,
            "event_image": "https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png",
            "event_name": "Basketball Tryout",
            "event_time": "Fri, 03 Nov 2023 14:00:00 GMT",
            "host_name": "John",
            "number_rater": 2,
            "position_address": "Exam Center"
        },
        "review_info": {
            "avg_rating": 4.0,
            "number_review": 2,
            "review_detail": [
                {
                    "rating": 5,
                    "review_comment": "Good spirit and so much fun",
                    "review_time": "Sun, 12 Nov 2023 12:50:44 GMT",
                    "review_user": "guitar"
                },
                {
                    "rating": 3,
                    "review_comment": "FUN FUN FUN",
                    "review_time": "Sun, 12 Nov 2023 12:50:44 GMT",
                    "review_user": "sam"
                }
            ]
        }
    }

    client = app.test_client()
    res = client.get('/detail/view_detail?event_id=2', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "OK", "data": test_data}

def test_view_comment_empty():
    client = app.test_client()
    res = client.get('/detail/view_review_detail?event_id=', headers=header)
    assert res.status_code == 401
    assert res.json == {"code": 401, "msg": "empty input date when should not be empty",
                        "data": []}
    
def test_view_comment_negative_event_id():
    client = app.test_client()
    res = client.get('/detail/view_review_detail?event_id=-1', headers=header)
    assert res.status_code == 401
    assert res.json == {"code": 401, "msg": "Negative event_id is not allowed",
                        "data": []}
    
def test_view_comment_not_existing_event_id():
    client = app.test_client()
    res = client.get('/detail/view_review_detail?event_id=100', headers=header)
    assert res.status_code == 401
    assert res.json == {"code": 401, "msg": "Event does not exist",
                        "data": []}
    
def test_add_comment_not_log_in():
    client = app.test_client()
    res = client.get('/detail/add_comment?event_id=1')
    assert res.status_code == 401
    assert res.json == {"code": 401, 'error': 'Authentication is required to access this resource'}


def test_login_then_add_comment():
    from backend.models.user_model import UserModel
    from backend import app, db, bcrypt
    # Create a user before testing login
    client = app.test_client()
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

    res = client.get('/detail/add_comment?event_id=')

    assert res.status_code == 401
    assert res.json == {"code": 401, "msg": "empty input date when should not be empty",
                        "data": []}

    assert response.status_code == 200
    assert 'token' in response.json

