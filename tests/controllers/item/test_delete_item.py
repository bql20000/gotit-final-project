import pytest

from tests.helpers import delete_item_demo, get_token


@pytest.mark.parametrize(
    'item_id, status_code',
    [
        # 401 - Unauthorized
        (1, 401)
    ]
)
def test_delete_item_401(client, item_id, status_code):
    # 401 - missing authorization header
    resp = delete_item_demo(client, item_id, token=None)
    assert resp.status_code == status_code
    assert resp.get_json() == {'message': 'Please log in first.',
                               'error_info': {}}

    # 401 - invalid token
    token = get_token(client, 'long', '1234') + 'noise'
    resp = delete_item_demo(client, item_id, token=token)
    assert resp.status_code == status_code
    assert resp.get_json() == {'message': 'Invalid token. Please log in again.',
                               'error_info': {}}
    
    
@pytest.mark.parametrize(
    'item_id, status_code, error',
    [
        # 404 - item not found
        (5, 404, {
            'message': 'Item with id 5 not found.',
            'error_info': {}
        })
    ]
)
def test_delete_item_404(client, item_id, status_code, error):
    token = get_token(client, 'long', '1234')
    resp = delete_item_demo(client, item_id, token=token)
    assert resp.status_code == status_code
    assert resp.get_json() == error


@pytest.mark.parametrize(
    'item_id, status_code, error',
    [
        # 403 - forbidden - not allowed to modify
        (3,
         403,
         {'message': 'You are not allowed to modify this item.',
          'error_info': {}
          })
    ]
)
def test_delete_item_403(client, item_id, status_code, error):
    token = get_token(client, 'long', '1234')
    resp = delete_item_demo(client, item_id, token=token)
    assert resp.status_code == status_code
    assert resp.get_json() == error


@pytest.mark.parametrize(
    'item_id, status_code',
    [
        # 200 - successful
        (1, 200)
    ]
)
def test_delete_item_200(client, item_id, status_code):
    token = get_token(client, 'long', '1234')
    resp = delete_item_demo(client, item_id, token=token)
    assert resp.status_code == status_code
    assert resp.get_json() == {}
