import pytest

from tests.helpers import get_item_demo


@pytest.mark.parametrize(
    'item_id, status_code',
    [
        # 200
        (1, 200)
    ]
)
def test_get_item_200(client, item_id, status_code):
    resp = get_item_demo(client, item_id)
    assert resp.status_code == status_code
    assert all(key in resp.get_json()
               for key in ['id', 'name', 'description', 'user_id',
                           'category_id', 'updated', 'created'])


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
def test_get_item_404(client, item_id, status_code, error):
    resp = get_item_demo(client, item_id)
    assert resp.status_code == status_code
    assert resp.get_json() == error
