import pytest

from tests.helpers import update_item_demo, get_token


@pytest.mark.parametrize(
    'item_id, request_data, status_code',
    [
        # 401 - Unauthorized
        (1, {'name': 'shoe', 'description': '', 'category_id': 1}, 401)
    ]
)
def test_update_item_401(client, item_id, request_data, status_code):
    # 401 - missing authorization header
    resp = update_item_demo(client, item_id, request_data, token=None)
    assert resp.status_code == status_code
    assert resp.get_json() == {'message': 'Please log in first.',
                               'error_info': {}}

    # 401 - invalid token
    token = get_token(client, 'long', '1234') + 'noise'
    resp = update_item_demo(client, item_id, request_data, token=token)
    assert resp.status_code == status_code
    assert resp.get_json() == {'message': 'Invalid token. Please log in again.',
                               'error_info': {}}


@pytest.mark.parametrize(
    'item_id, request_data, status_code, error',
    [
        # 400 - name's first char is number
        (1,
         {'name': '1shoe', 'description': '', 'category_id': 1},
         400,
         {'message': 'Invalid request data.',
          'error_info': {
              'name': ['First character must not be a number.']
          }}),

        # 400 - name length = 0 && description length > 255
        (1,
         {'name': '', 'description': 'a' * 256, 'category_id': 1},
         400,
         {'message': 'Invalid request data.',
          'error_info': {
              'name': ['Length must be between 1 and 32.'],
              'description': ['Longer than maximum length 255.']
          }}),

        # 400 - name length > 32 && category not found
        (1,
         {'name': 'a' * 33, 'description': '', 'category_id': 4},
         400,
         {'message': 'Invalid request data.',
          'error_info': {
              'name': ['Length must be between 1 and 32.'],
              'category_id': ['Category with id 4 not found.']
          }}),

        # 400 - name existed in the category
        (1,
         {'name': 'racket', 'description': '', 'category_id': 2},
         400,
         {'message': 'This category has already had item racket.',
          'error_info': {}
          }),
    ]
)
def test_update_item_400(client, item_id, request_data, status_code, error):
    token = get_token(client, 'long', '1234')
    resp = update_item_demo(client, item_id, request_data, token=token)
    assert resp.status_code == status_code
    assert resp.get_json() == error


@pytest.mark.parametrize(
    'item_id, request_data, status_code, error',
    [
        # 404 - item not found
        (5,
         {'name': 'shoe', 'description': '', 'category_id': 1},
         404,
         {'message': 'Item with id 5 not found.',
          'error_info': {}
          })
    ]
)
def test_update_item_404(client, item_id, request_data, status_code, error):
    token = get_token(client, 'long', '1234')
    resp = update_item_demo(client, item_id, request_data, token=token)
    assert resp.status_code == status_code
    assert resp.get_json() == error


@pytest.mark.parametrize(
    'item_id, request_data, status_code, error',
    [
        # 403 - forbidden - not allowed to modify
        (3,
         {'name': 'shoe', 'description': '', 'category_id': 2},
         403,
         {'message': 'You are not allowed to modify this item.',
          'error_info': {}
          })
    ]
)
def test_update_item_403(client, item_id, request_data, status_code, error):
    token = get_token(client, 'long', '1234')
    resp = update_item_demo(client, item_id, request_data, token=token)
    assert resp.status_code == status_code
    assert resp.get_json() == error


@pytest.mark.parametrize(
    'item_id, request_data, status_code',
    [
        # 200 - successful & duplicate item name but different category
        (1, {'name': 'ball', 'description': '', 'category_id': 2}, 200)
    ]
)
def test_update_item_200(client, item_id, request_data, status_code):
    token = get_token(client, 'long', '1234')
    resp = update_item_demo(client, item_id, request_data, token=token)
    assert resp.status_code == status_code
    assert all(key in resp.get_json()
               for key in ['id', 'name', 'description', 'user_id',
                           'category_id', 'updated', 'created'])
