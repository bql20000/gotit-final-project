import pytest

from tests.helpers import create_item_demo, get_token


@pytest.mark.parametrize(
    'request_data, status_code',
    [
        # 401 - Unauthorized
        ({'name': 'shoe', 'description': '', 'category_id': 1}, 401)
    ]
)
def test_create_item_401(client, request_data, status_code):
    # 401 - missing authorization header
    resp = create_item_demo(client, request_data, token=None)
    assert resp.status_code == status_code
    assert resp.get_json() == {'message': 'Please log in first.',
                               'error_info': {}}

    # 401 - invalid token
    token = get_token(client, 'long', '1234') + 'noise'
    resp = create_item_demo(client, request_data, token=token)
    assert resp.status_code == status_code
    assert resp.get_json() == {'message': 'Invalid token. Please log in again.',
                               'error_info': {}}


@pytest.mark.parametrize(
    'request_data, status_code, error',
    [
        # 400 - name's first char is number
        ({'name': '1shoe', 'description': '', 'category_id': 1},
         400,
         {'message': 'Invalid request data.',
          'error_info': {
              'name': ['First character must not be a number.']
          }}),

        # 400 - name length = 0 && description length > 255
        ({'name': '', 'description': 'a' * 256, 'category_id': 1},
         400,
         {'message': 'Invalid request data.',
          'error_info': {
              'name': ['Length must be between 1 and 32.'],
              'description': ['Longer than maximum length 255.']
          }}),

        # 400 - name length > 32 && category not found
        ({'name': 'a' * 33, 'description': '', 'category_id': 4},
         400,
         {'message': 'Invalid request data.',
          'error_info': {
              'name': ['Length must be between 1 and 32.'],
              'category_id': ['Category with id 4 not found.']
          }}),

        # 400 - name existed in the category
        ({'name': 'ball', 'description': '', 'category_id': 1},
         400,
         {'message': 'This category has already had item ball.',
          'error_info': {}
          }),
    ]
)
def test_create_item_400(client, request_data, status_code, error):
    token = get_token(client, 'long', '1234')
    resp = create_item_demo(client, request_data, token=token)
    assert resp.status_code == status_code
    assert resp.get_json() == error


@pytest.mark.parametrize(
    'request_data, status_code',
    [
        # 201 - Name length = 1 7 description length = 0
        ({'name': 'a', 'description': '', 'category_id': 1}, 201),

        # 201 - item name existed, but different category
        ({'name': 'ball', 'description': '', 'category_id': 2}, 201),
    ]
)
def test_create_item_201(client, request_data, status_code):
    token = get_token(client, 'long', '1234')
    resp = create_item_demo(client, request_data, token=token)
    assert resp.status_code == status_code
    assert all(key in resp.get_json()
               for key in ['id', 'name', 'description', 'updated',
                           'created', 'category_id', 'user_id'])
