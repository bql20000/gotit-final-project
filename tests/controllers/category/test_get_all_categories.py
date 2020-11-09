import pytest

from tests.helpers import get_all_category_demo


@pytest.mark.parametrize(
    'status_code',
    [
        # 200
        200,
    ]
)
def test_get_all_category_200(client, status_code):
    resp = get_all_category_demo(client)
    assert resp.status_code == status_code
    assert len(resp.get_json()) == 2
    assert all(key in resp.get_json()[0]
               for key in ['id', 'name', 'updated', 'created'])
