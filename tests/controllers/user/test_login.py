import pytest

from tests.helpers import login_demo


@pytest.mark.parametrize(
    'request_data, status_code, error',
    [
        # 401 - wrong username
        ({'username': 'longg', 'password': '1234'},
         401,
         {'message': 'Wrong username or password.',
          'error_info': {}
          }),

        # 401 - wrong password
        ({'username': 'long', 'password': '12334'},
         401,
         {'message': 'Wrong username or password.',
          'error_info': {}
          }),
    ]
)
def test_login_401(client, request_data, status_code, error):
    resp = login_demo(client, request_data)
    assert resp.status_code == status_code
    assert resp.get_json() == error


@pytest.mark.parametrize(
    'request_data, status_code',
    [
        # 200 - succeed with jwt token returned
        ({'username': 'long', 'password': '1234'}, 200),
    ]
)
def test_login_200(client, request_data, status_code):
    resp = login_demo(client, request_data)
    assert resp.status_code == status_code
    assert all(key in resp.get_json()
               for key in ['access_token', 'token_type'])
