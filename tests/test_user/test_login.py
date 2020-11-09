import pytest

from tests.helpers import login_demo


@pytest.mark.parametrize(
    'request_data, status_code, error',
    [
        # 400 - wrong username
        ({'username': 'longg', 'password': '1234'},
         400,
         {'message': 'Wrong username or password.',
          'error_info': {}
          }),

        # 400 - wrong password
        ({'username': 'long', 'password': '12334'},
         400,
         {'message': 'Wrong username or password.',
          'error_info': {}
          }),
    ]
)
def test_login_400(client, request_data, status_code, error):
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
    assert 'access_token' in resp.get_json()
    assert 'token_type' in resp.get_json()
