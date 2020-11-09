import pytest

from tests.helpers import create_category_demo


@pytest.mark.parametrize(
    'request_data, status_code, error',
    [
        # 400 - name existed
        ({'name': 'soccer'}, 400, {
            'message': 'Category soccer existed.',
            'error_info': {}
        }),

        # 400 - name starts with a number
        ({'name': '1occer'}, 400, {
            'message': 'Invalid request data.',
            'error_info': {
                'name': 'First character must not be a number.'
            }
        }),

        # 400 - name length = 0
        ({'name': ''}, 400, {
            'message': 'Invalid request data.',
            'error_info': {
                'name': ['Length must be between 1 and 32.']
            }
        }),
    ]
)
def test_create_category_400(client, request_data, status_code, error):
    resp = create_category_demo(client, request_data)
    assert resp.status_code == status_code
    assert resp.get_json() == error


@pytest.mark.parametrize(
    'request_data, status_code',
    [
        # 201 - successful & name length = 32
        ({'name': 'a' * 32}, 201)
    ]
)
def test_create_category_201(client, request_data, status_code):
    resp = create_category_demo(client, request_data)
    assert resp.status_code == status_code
    assert all(key in resp.get_json()
               for key in ['id', 'name', 'updated', 'created'])
