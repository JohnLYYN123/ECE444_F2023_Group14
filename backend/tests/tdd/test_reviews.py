from backend import app

header = {"Authorization": "eyJ1c2VyX2lkIjoxLCJ1b2Z0X2VtYWlsIjoiZ3VpdGFyLmhlcm9AbWFpbC51dG9yb250by5jYSJ9.ZVEhJw.L8uu9748wABRiu7cpVo4U45Uzyg"}

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