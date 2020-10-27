def register_demo(client, username, password):
    return client.post('/register', json={"username": username, "password": password})


def test_register(init_client, init_db):
    """Register some users with valid/invalid request data."""

    # successful
    resp = register_demo(init_client, 'long', '1234')
    assert resp.status_code == 201
    assert resp.get_json().get('message') == 'User registers successfully!'

    # username existed
    resp = register_demo(init_client, 'long', '2345')
    assert resp.status_code == 400
    assert resp.get_json().get('messages')[0] == 'Username existed, please choose another username.'


def login_demo(client, username, password):
    return client.post('/login', json={"username": username, "password": password})


def test_login(init_client, init_db):
    """Login several times with different scenarios"""

    # register one user first
    register_demo(init_client, 'thinh', '1234')

    # wrong username
    resp = login_demo(init_client, 'thinh_suy', '1234')
    assert resp.status_code == 400
    assert resp.get_json().get('message') == 'Wrong username or password.'

    # wrong password
    resp = login_demo(init_client, 'thinh', 'asdf')
    assert resp.status_code == 400
    assert resp.get_json().get('message') == 'Wrong username or password.'

    # correct
    resp = login_demo(init_client, 'thinh', '1234')
    assert resp.status_code == 200
    assert resp.get_json().get('message') == 'Successfully logged in.'
