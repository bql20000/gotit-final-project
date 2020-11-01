from app.models.user import UserModel
from app.models.category import CategoryModel
from app.models.item import ItemModel


def init_users():
    """Create 2 sample users."""
    UserModel('thinh', '1234').save_to_db()
    UserModel('long', '1234').save_to_db()


def init_categories():
    """Create 2 sample categories."""
    CategoryModel('soccer').save_to_db()
    CategoryModel('badminton').save_to_db()


def init_items():
    """Create 4 sample items, 2 for each sample user and category."""
    ItemModel('ball', 'A ball', 1, 1).save_to_db()
    ItemModel('grass', "Some grass", 1, 1).save_to_db()
    ItemModel('racket', "A racket", 2, 2).save_to_db()
    ItemModel('net', "A ", 2, 2).save_to_db()


def create_db_samples():
    """Execute all the sample creations."""
    init_users()
    init_categories()
    init_items()


def register_demo(client, username, password):
    """Return a response object received by the client after making a
    HTTP post request to register.
    """
    return client.post('/register', json={'username': username, 'password': password})


def login_demo(client, username, password):
    """Return a response object received by the client after making a
    HTTP post request to login.
    """
    return client.post('/login', json={'username': username, 'password': password})


def create_category_demo(client, name):
    """Return a response object received by the client after making a
    HTTP post request to create a category.
    """
    return client.post('/categories', json={'name': name})


def create_item_demo(client, token, name, description, category_id):
    """Return a response object received by the client after making a
    HTTP post request to create an item.
    """

    return client.post('/items',
                       json={'name': name,
                             'description': description,
                             'category_id': category_id},
                       headers={'AUTHORIZATION': token}
                       )


def update_item_demo(client, token, item_id, name, description, category_id):
    """Return a response object received by the client after making a
    HTTP put request to update an item.
    """

    return client.put(f'/items/{item_id}',
                      json={"name": name,
                            'description': description,
                            'category_id': category_id},
                      headers={'AUTHORIZATION': token}
                      )


def request_page_demo(client, category_id, page_number, items_per_page):
    """Return a response object received by the client after making a
    HTTP post request to retrieve a list of item.
    The item list is determined by page_number & items_per_page provided
    by the client.
    """

    return client.post(f'/categories/{category_id}/items',
                       json={'page_number': page_number,
                             'items_per_page': items_per_page})

