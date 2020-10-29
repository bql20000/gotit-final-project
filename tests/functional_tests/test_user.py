from tests.helpers import login_demo, register_demo


def test_register(init_client, init_db):
    """Register some users with valid/invalid request data."""

    # successful
    resp = register_demo(init_client, 'some_user', '1234')
    assert resp.status_code == 201
    assert resp.get_json()['username'] == 'some_user'

    # username existed
    resp = register_demo(init_client, 'long', '2345')
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Username existed.'
    assert not resp.get_json()['error_info']

    # username & password length < 4
    resp = register_demo(init_client, 'lon', '123')
    assert resp.status_code == 400
    resp.get_json()['message'] = 'Invalid request data.'
    assert resp.get_json()['error_info']['username'][0] == 'Length must be between 4 and 32.'
    assert resp.get_json()['error_info']['password'][0] == 'Length must be between 4 and 32.'

    # username & password length > 32
    long_name = 'a' * 33
    long_password = '1' * 33
    resp = register_demo(init_client, long_name, long_password)
    assert resp.status_code == 400
    resp.get_json()['message'] = 'Invalid request data.'
    assert resp.get_json()['error_info']['username'][0] == 'Length must be between 4 and 32.'

    # username & password length = 32
    long_name = 'a' * 32
    long_password = '1' * 32
    resp = register_demo(init_client, long_name, long_password)
    assert resp.status_code == 201
    resp.get_json()['username'] = long_name


def test_login(init_client, init_db):
    """Login several times with different scenarios"""

    # wrong username
    resp = login_demo(init_client, 'longgg', '1234')
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Wrong username or password.'

    # wrong password
    resp = login_demo(init_client, 'long', '1233')
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Wrong username or password.'

    # correct
    resp = login_demo(init_client, 'long', '1234')
    assert resp.status_code == 200
    assert resp.get_json().get('jwt_token')
