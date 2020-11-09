from flaskr.models.user import UserModel
from flaskr.models.category import CategoryModel
from flaskr.models.item import ItemModel


def init_users():
    """Create 2 sample users."""
    UserModel('long', '1234').save_to_db()
    UserModel('thinh', '1234').save_to_db()


def init_categories():
    """Create 2 sample categories."""
    CategoryModel('soccer').save_to_db()
    CategoryModel('badminton').save_to_db()


def init_items():
    """Create 4 sample items, 2 for each sample user and category."""
    ItemModel('ball', 'A ball', 1, 1).save_to_db()
    ItemModel('grass', 'Some grass', 1, 1).save_to_db()
    ItemModel('racket', 'A racket', 2, 2).save_to_db()
    ItemModel('net', "A ", 2, 2).save_to_db()


def create_db_samples():
    """Execute all the sample creations."""
    init_users()
    init_categories()
    init_items()


def register_demo(client, request_data):
    """Return a response object received by the client after making a
    HTTP POST request to register.
    """
    return client.post('/register', json=request_data)


def login_demo(client, request_data):
    """Return a response object received by the client after making a
    HTTP POST request to login.
    """
    return client.post('/login', json=request_data)


def get_category_demo(client, category_id):
    """Return a response object received by the client after making a
    HTTP GET to get a category's information.
    """
    return client.get(f'/categories/{category_id}')


def create_category_demo(client, data):
    """Return a response object received by the client after making a
    HTTP POST request to create a category.
    """
    return client.post('/categories', json=data)


def get_all_category_demo(client):
    """Return a response object received by the client after making a
    HTTP GET request to get all categories.
    """
    return client.get('/categories')


def get_item_demo(client, item_id):
    """Return a response object received by the client after making a
    HTTP GET to get an item's information.
    """
    return client.get(f'/items/{item_id}')


def create_item_demo(client, request_data, token=None):
    """Return a response object received by the client after making a
    HTTP POST request to create an item.
    """
    if token:
        return client.post('/items',
                           json=request_data,
                           headers={'AUTHORIZATION': f'Bearer {token}'})
    else:
        return client.post('/items', json=request_data)


def update_item_demo(client, item_id, request_data, token=None):
    """Return a response object received by the client after making a
    HTTP PUT request to create an item.
    """
    if token:
        return client.put(f'/items/{item_id}',
                          json=request_data,
                          headers={'AUTHORIZATION': f'Bearer {token}'})
    else:
        return client.put(f'/items/{item_id}', json=request_data)


def delete_item_demo(client, item_id, token=None):
    """Return a response object received by the client after making a
    HTTP PUT request to create an item.
    """
    if token:
        return client.delete(f'/items/{item_id}',
                             headers={'AUTHORIZATION': f'Bearer {token}'})
    else:
        return client.delete(f'/items/{item_id}')


def request_page_demo(client, category_id, page_number, items_per_page):
    """Return a response object received by the client after making a
    HTTP GET request to retrieve a list of item.
    The item list is determined by page_number & items_per_page provided
    in the query string.
    """
    return client.get(f'/categories/{category_id}/items'
                      f'?page_number={page_number}&items_per_page={items_per_page}')


def get_token(client, username, password):
    return login_demo(client, {'username': username, 'password': password}
                      ).get_json()['access_token']
