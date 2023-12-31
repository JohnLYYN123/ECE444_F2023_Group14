from backend import app
import pytest

header = {"Authorization": 'eyJ1c2VyX2lkIjoxLCJ1b2Z0X2VtYWlsIjoiZ3VpdGFyLmhlcm9AbWFpbC51dG9yb250by5jYSJ9.ZVEhJw.L8uu9748wABRiu7cpVo4U45Uzyg'}


def test_no_authentication():
    client = app.test_client()
    res = client.get('/main_sys/filter?title=')
    assert res.status_code == 401
    assert res.json == {"code": 401, "error": "Authentication is required to access this resource"}

def test_invalid_title():
    client = app.test_client()
    res = client.get('/main_sys/filter?title=SPORTS', headers=header)
    assert res.status_code == 401
    assert res.json == {"code": 401,
                        "msg": "filter does not exist", "data": []}


def test_not_exist_title():
    client = app.test_client()
    res = client.get('/main_sys/filter?title=study', headers=header)
    assert res.status_code == 401
    assert res.json == {"code": 401,
                        "msg": "filter does not exist", "data": []}


def test_valid_filter():
    client = app.test_client()
    res = client.get('/main_sys/filter?title=art', headers=header)

    test_data = [{'average_rating': 3.5,
           'description': 'help student with ECE444 project and have a secret '
                          'party',
           'event_id': 1,
           'event_image': 'https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png',
           'event_name': 'ECE444 project UX help session',
           'event_time': 'Mon, 04 Nov 2024 14:00:00 GMT',
           'filter': 'art'},
          {'average_rating': 3.5,
           'description': 'help student with ECE444 project and have a secret '
                          'party',
           'event_id': 2,
           'event_image': 'https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png',
           'event_name': 'ECE444 project UX help session 2',
           'event_time': 'Sat, 04 Nov 2023 14:00:00 GMT',
           'filter': 'art'},
          {'average_rating': 3.5,
           'description': 'help student with ECE444 project and have a secret '
                          'party',
           'event_id': 3,
           'event_image': 'https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png',
           'event_name': 'ECE444 project UX help session 3',
           'event_time': 'Sun, 05 Nov 2023 14:00:00 GMT',
           'filter': 'art'},
          {'average_rating': 3.5,
           'description': 'help student with ECE444 project and have a secret '
                          'party',
           'event_id': 4,
           'event_image': 'https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png',
           'event_name': 'ECE444 project UX help session 4',
           'event_time': 'Mon, 06 Nov 2023 14:00:00 GMT',
           'filter': 'art'},
          {'average_rating': 3.5,
           'description': 'help student with ECE444 project and have a secret '
                          'party',
           'event_id': 5,
           'event_image': 'https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png',
           'event_name': 'ECE444 project UX help session 5',
           'event_time': 'Tue, 07 Nov 2023 14:00:00 GMT',
           'filter': 'art'},
          {'average_rating': 5.0,
           'description': 'Excellent filming experiences with Mr.Jerry',
           'event_id': 9,
           'event_image': 'https://th.bing.com/th/id/OIP.xtzZpD9co7u3S6jU9J1ZPwHaE8?pid=ImgDet&rs=1',
           'event_name': 'Filming and CGI',
           'event_time': 'Thu, 30 Nov 2023 14:00:00 GMT',
           'filter': 'art'}]

    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "OK", "data": test_data}


def test_valid_filter_valid_search_value():
    test_data = [{'average_rating': 3.5,
           'description': 'help student with ECE444 project and have a secret '
                          'party',
           'event_id': 1,
           'event_image': 'https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png',
           'event_name': 'ECE444 project UX help session',
           'event_time': 'Mon, 04 Nov 2024 14:00:00 GMT',
           'filter': 'art'},
          {'average_rating': 3.5,
           'description': 'help student with ECE444 project and have a secret '
                          'party',
           'event_id': 2,
           'event_image': 'https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png',
           'event_name': 'ECE444 project UX help session 2',
           'event_time': 'Sat, 04 Nov 2023 14:00:00 GMT',
           'filter': 'art'},
          {'average_rating': 3.5,
           'description': 'help student with ECE444 project and have a secret '
                          'party',
           'event_id': 3,
           'event_image': 'https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png',
           'event_name': 'ECE444 project UX help session 3',
           'event_time': 'Sun, 05 Nov 2023 14:00:00 GMT',
           'filter': 'art'},
          {'average_rating': 3.5,
           'description': 'help student with ECE444 project and have a secret '
                          'party',
           'event_id': 4,
           'event_image': 'https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png',
           'event_name': 'ECE444 project UX help session 4',
           'event_time': 'Mon, 06 Nov 2023 14:00:00 GMT',
           'filter': 'art'},
          {'average_rating': 3.5,
           'description': 'help student with ECE444 project and have a secret '
                          'party',
           'event_id': 5,
           'event_image': 'https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png',
           'event_name': 'ECE444 project UX help session 5',
           'event_time': 'Tue, 07 Nov 2023 14:00:00 GMT',
           'filter': 'art'},
          {'average_rating': 5.0,
           'description': 'Excellent filming experiences with Mr.Jerry',
           'event_id': 9,
           'event_image': 'https://th.bing.com/th/id/OIP.xtzZpD9co7u3S6jU9J1ZPwHaE8?pid=ImgDet&rs=1',
           'event_name': 'Filming and CGI',
           'event_time': 'Thu, 30 Nov 2023 14:00:00 GMT',
           'filter': 'art'}]

    client = app.test_client()
    res = client.get('/main_sys/filter?title=art&search_value=', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "OK", "data": test_data}


def test_valid_filter_empty_search_value():
    test_data = []

    client = app.test_client()
    res = client.get('/main_sys/filter?title=art&search_value=basketball', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "OK", "data": test_data}


def test_valid_filter_valid_search_value_2():
    client = app.test_client()
    res = client.get('/main_sys/filter?title=art&search_value=random', headers=header)
    assert res.status_code == 200
    assert res.json == {"code": 200, "msg": "OK", "data": []}


def test_emp_string():
    client = app.test_client()
    res = client.get('/main_sys/filter?title=', headers=header)
    assert res.status_code == 401
    assert res.json == {"code": 401, "msg": "No filter applied", "data": []}

