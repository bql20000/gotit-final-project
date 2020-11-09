from tests.helpers import get_all_category_demo


def test_get_all_category_200(client):
    resp = get_all_category_demo(client)
    assert resp.status_code == 200
    assert len(resp.get_json()) == 2
    assert all(key in resp.get_json()[0]
               for key in ['id', 'name', 'updated', 'created'])
