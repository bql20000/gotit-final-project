import pytest

from tests.helpers import get_items_demo, create_item_demo, get_token


@pytest.mark.parametrize(
    'category_id, page_number, items_per_page, status_code, error',
    [
        # 400 - page_number <= 0 || items_per_page <= 0
        (1, -1, 0, 400,
         {'message': 'Invalid request data.',
          'error_info': {
              'page_number': ['Must be greater than or equal to 1.'],
              'items_per_page': ['Must be greater than or equal to 1.']
          }}),
    ]
)
def test_get_items_400(client, category_id, page_number, items_per_page, status_code, error):
    resp = get_items_demo(client, category_id, page_number, items_per_page)
    assert resp.status_code == status_code
    assert resp.get_json() == error


@pytest.mark.parametrize(
    'category_id, page_number, items_per_page, status_code, error',
    [
        # 404 - category not found
        (3, 1, 2, 404,
         {'message': 'Category with id 3 not found.',
          'error_info': {}
          }),
    ]
)
def test_get_items_404(client, category_id, page_number, items_per_page, status_code, error):
    resp = get_items_demo(client, category_id, page_number, items_per_page)
    assert resp.status_code == status_code
    assert resp.get_json() == error


@pytest.mark.parametrize(
    'category_id, page_number, items_per_page, status_code',
    [
        # 200 - page with no items
        (1, 5, 3, 200),

        # 200 - a normal page with number of items returns = items_per_page
        (1, 2, 3, 200),

        # 200 - last page with number of items returned < items_per_page
        (1, 3, 4, 200),
    ]
)
def test_get_items_200(client, category_id, page_number, items_per_page, status_code):
    # Add more 8 items to category 1 to get 10 in total
    token = get_token(client, 'long', '1234')
    for i in range(8):
        data = {'name': f'bike{i}',
                'description': '',
                'category_id': 1}
        create_item_demo(client, data, token=token)

    resp = get_items_demo(client, category_id, page_number, items_per_page)

    assert resp.status_code == status_code
    total_pages = 10 // items_per_page + (10 % items_per_page > 0)
    assert resp.get_json()['total_pages'] == total_pages
    assert resp.get_json()['total_items'] == 10
    assert resp.get_json()['current_page'] == page_number
    assert resp.get_json()['items_per_page'] == items_per_page
    if page_number > total_pages:
        assert len(resp.get_json()['items']) == 0
    elif page_number == total_pages and 10 % items_per_page:
        assert len(resp.get_json()['items']) == 10 % items_per_page
    else:
        assert len(resp.get_json()['items']) == items_per_page
