import pytest

from tests.helpers import get_category_demo


@pytest.mark.parametrize(
    'category_id, status_code',
    [
        # 200
        (1, 200),
    ]
)
def test_get_category_200(client, category_id, status_code):
    resp = get_category_demo(client, category_id)
    assert resp.status_code == status_code
    assert all(key in resp.get_json() for key in ['id', 'name', 'updated', 'created'])


@pytest.mark.parametrize(
    'category_id, status_code, error',
    [
        # 404 - category not found
        (3, 404, {
            'message': 'Category with id 3 not found.',
            'error_info': {}
        }),
    ]
)
def test_get_category_404(client, category_id, status_code, error):
    resp = get_category_demo(client, category_id)
    assert resp.status_code == status_code
    assert resp.get_json() == error
