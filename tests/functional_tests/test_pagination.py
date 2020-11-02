from tests.helpers import login_demo, create_item_demo, request_page_demo


def test_request_page(init_client, init_db):
    """Request a page specified by 2 parameters: page_number and items_per_page.

    After testing at test_item, category 1 has 5 items, category 2 has 2 items.
    Check total number of items by the followings:
        from app.models.item import ItemModel
        print(len(ItemModel.query.all()))
    """

    # add 5 items for category 1 (soccer) --> category soccer has 10 items in total
    token = login_demo(init_client, 'long', '1234').get_json()['jwt_token']
    for i in range(5):
        create_item_demo(init_client, token, f'new_item{i}', 'some_description', 1)

    category_id = 1
    page_number = 0
    items_per_page = -1

    # 400 - page_number <= 0 || items_per_page <= 0
    resp = request_page_demo(init_client, category_id, page_number, items_per_page)
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Invalid request data.'
    assert resp.get_json()['error_info']['page_number'][0] == 'Must be greater than or equal to 1.'
    assert resp.get_json()['error_info']['items_per_page'][0] == 'Must be greater than or equal to 1.'

    page_number = 2
    items_per_page = 3

    # 404 - category not found
    category_id = 0
    resp = request_page_demo(init_client, category_id, page_number, items_per_page)
    assert resp.status_code == 404
    assert resp.get_json()['message'] == f'Category with id {category_id} not found.'

    # 200 - successful - a normal page with number of items returns = items_per_page
    # 10 items / 4 pages -->  3 - 3 - 3 - 1
    category_id = 1
    resp = request_page_demo(init_client, category_id, page_number, items_per_page)
    assert resp.status_code == 200
    assert resp.get_json()['total_items'] == 10
    assert resp.get_json()['total_pages'] == 4
    assert resp.get_json()['current_page'] == 2
    assert resp.get_json()['items_per_page'] == 3
    assert len(resp.get_json()['items']) == 3

    # 200 - successful - last page with number of items returned < items_per_page
    # 10 items / 3 pages -->  4 - 4 - 2
    category_id = 1
    page_number = 3
    items_per_page = 4
    resp = request_page_demo(init_client, category_id, page_number, items_per_page)
    assert resp.status_code == 200
    assert resp.get_json()['total_items'] == 10
    assert resp.get_json()['total_pages'] == 3
    assert resp.get_json()['current_page'] == 3
    assert resp.get_json()['items_per_page'] == 4
    assert len(resp.get_json()['items']) == 2
