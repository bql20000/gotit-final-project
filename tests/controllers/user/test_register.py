import pytest

from tests.helpers import register_demo


@pytest.mark.parametrize(
    'request_data, status_code',
    [
        # 201 - username has '_' character
        ({'username': 'maxu', 'password': '1234'}, 201),

        # 201 - username & password length = 32
        ({'username': 'a' * 32, 'password': '1' * 32}, 201)
    ]
)
def test_register_201(client, request_data, status_code):
    resp = register_demo(client, request_data)
    assert resp.status_code == status_code
    assert all(key in resp.get_json()
               for key in ['username', 'updated', 'created'])
    assert 'password' not in resp.get_json()


@pytest.mark.parametrize(
    'request_data, status_code, error',
    [
        # 400 - username existed
        ({'username': 'long', 'password': '1234'},
         400,
         {'message': 'Username existed.',
          'error_info': {}
          }),

        # 400 - username length < 4 & password length < 32
        ({'username': 'abc', 'password': '1'*33},
         400,
         {'message': 'Invalid request data.',
          'error_info': {
              'username': ['Length must be between 4 and 32.'],
              'password': ['Length must be between 4 and 32.']
          }}),

        # 400 - username contains special character ' '
        ({'username': 'abc ', 'password': '1234'},
         400,
         {'message': 'Invalid request data.',
          'error_info': {
              'username': ['Username must not contain special characters (except _).'],
          }}),

        # 400 - username begins with a number
        ({'username': '1abc', 'password': '1234'},
         400,
         {'message': 'Invalid request data.',
          'error_info': {
              'username': ['First character must not be a number.'],
          }})
    ]
)
def test_register_400(client, request_data, status_code, error):
    resp = register_demo(client, request_data)
    assert resp.status_code == status_code
    assert resp.get_json() == error
