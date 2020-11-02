from tests.helpers import login_demo, create_item_demo, update_item_demo


def test_get_item_by_id(init_client, init_db):
    """Test getting an item by its id in different scenarios."""
    test_id = 1
    resp = init_client.get(f'/items/{test_id}')
    assert resp.status_code == 200
    assert resp.get_json()['name'] == 'ball'
    assert resp.get_json()['description'] == 'A ball'
    assert resp.get_json()['id'] == test_id
    assert resp.get_json()['user_id'] == 1

    test_id = 0
    resp = init_client.get(f'/items/{test_id}')
    assert resp.status_code == 404
    assert resp.get_json()['message'] == f'Item with id {test_id} not found.'


def test_create_item(init_client, init_db):
    """Test creating an item by its id in different scenarios."""

    # user long with id 2 log in to get a valid token
    token = login_demo(init_client, 'long', '1234').get_json()['jwt_token']

    test_name = 'some_item'
    test_description = 'some_description'
    test_category_id = 1

    # 401 - without logging in (without access token)
    resp = init_client.post('/items',
                            json={'name': test_name,
                                  'description': test_description,
                                  'category_id': test_category_id}
                            )
    assert resp.status_code == 401
    assert resp.get_json()['message'] == 'Please log in first.'

    # 401 - Invalid token
    resp = create_item_demo(init_client, token + '?', test_name, test_description, test_category_id)
    assert resp.status_code == 401
    assert resp.get_json()['message'] == 'Invalid token. Please log in again.'

    # 400 - Item name existed
    resp = create_item_demo(init_client, token, 'ball', test_description, test_category_id)
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Item ball existed.'

    # 400 - First name character is a number
    resp = create_item_demo(init_client, token, '1ball', test_description, test_category_id)
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Invalid request data.'
    assert resp.get_json()['error_info']['name'][0] == 'First character must not be a number.'

    # 400 - Item name length = 0 && description length > 255
    test_name = ''
    test_description = 'a' * 256
    resp = create_item_demo(init_client, token, test_name, test_description, test_category_id)
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Invalid request data.'
    assert resp.get_json()['error_info']['name'][0] == 'Length must be between 1 and 32.'
    assert resp.get_json()['error_info']['description'][0] == 'Longer than maximum length 255.'

    # 400 - Item name length > 32 && Not found category with id = category_id
    test_name = 'a' * 33
    test_category_id = 0
    resp = create_item_demo(init_client, token, test_name, test_description, test_category_id)
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Invalid request data.'
    assert resp.get_json()['error_info']['name'][0] == 'Length must be between 1 and 32.'
    assert resp.get_json()['error_info']['category_id'][0] == f'Category with id {test_category_id} not found.'

    # 200 - Item name length = 32 & description length = 255
    test_name = 'a' * 32
    test_description = 'a' * 255
    test_category_id = 1
    resp = create_item_demo(init_client, token, test_name, test_description, test_category_id)
    assert resp.status_code == 201
    assert resp.get_json()['id'] == 5      # after 4 sample items
    assert resp.get_json()['name'] == test_name
    assert resp.get_json()['description'] == test_description
    assert resp.get_json()['user_id'] == 2      # user long has id = 2

    # 200 - Item name length = 1 & description length = 0
    test_name = 'X'
    test_description = ''
    resp = create_item_demo(init_client, token, test_name, test_description, test_category_id)
    assert resp.status_code == 201
    assert resp.get_json()['id'] == 6    # after 4 sample items + 1 above item
    assert resp.get_json()['name'] == test_name
    assert resp.get_json()['description'] == test_description
    assert resp.get_json()['user_id'] == 2      # user long has id = 2


def test_update_item(init_client, init_db):
    """Test updating an item by its id in different scenarios."""

    # user long with id 2 log in to get a valid token
    token = login_demo(init_client, 'long', '1234').get_json()['jwt_token']

    test_name = 'some_item'
    test_description = 'some_description'
    test_category_id = 1
    test_id = 1

    # 404 - item with id = test_id not found
    test_id = 0
    resp = update_item_demo(init_client, token, test_id, test_name, test_description, test_category_id)
    assert resp.status_code == 404
    assert resp.get_json()['message'] == f'Item with id {test_id} not found.'

    # 403 - not allowed to modify (ownership required)
    test_id = 1  # user 2 only own item 3,4
    resp = update_item_demo(init_client, token, test_id, test_name, test_description, test_category_id)
    assert resp.status_code == 403
    assert resp.get_json()['message'] == 'You are not allowed to modify this item.'

    # 400 - new item's name already exists
    test_name = 'grass'
    test_id = 3
    resp = update_item_demo(init_client, token, test_id, test_name, test_description, test_category_id)
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Item grass existed.'

    # 200 - successful
    test_name = 'racket'
    test_description = 'An updated racket'
    test_id = 3
    test_category_id = 2
    resp = update_item_demo(init_client, token, test_id, test_name, test_description, test_category_id)
    assert resp.status_code == 200
    assert resp.get_json()['name'] == test_name
    assert resp.get_json()['description'] == test_description
    assert resp.get_json()['id'] == test_id
    assert resp.get_json()['user_id'] == 2


def test_delete_item(init_client, init_db):
    """Test updating an item by its id in different scenarios."""

    # user long with id 2 log in to get a valid token
    token = login_demo(init_client, 'long', '1234').get_json()['jwt_token']

    # 404 - item with id = test_id not found
    test_id = 0
    resp = init_client.delete(f'/items/{test_id}', headers={'AUTHORIZATION': token})
    assert resp.status_code == 404
    assert resp.get_json()['message'] == f'Item with id {test_id} not found.'

    # 403 - not allowed to modify (ownership required)
    test_id = 1  # user 2 only own item 3,4
    resp = init_client.delete(f'/items/{test_id}', headers={'AUTHORIZATION': token})
    assert resp.status_code == 403
    assert resp.get_json()['message'] == 'You are not allowed to modify this item.'

    test_id = 3
    resp = init_client.delete(f'/items/{test_id}', headers={'AUTHORIZATION': token})
    assert resp.status_code == 200
    assert not resp.get_json()
