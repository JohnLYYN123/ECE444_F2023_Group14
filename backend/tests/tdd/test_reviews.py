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
    mock_data = {
        "comment": "testcomment",
        "rating": 5
    }

    client = app.test_client()
    res = client.post('/detail/add_comment?event_id=1', json=mock_data, headers=header)

    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "INSERTED", "response_data": {"comment": "testcomment", "rating": 5}}
