from functools import wraps

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
    return client.post('/register', json={"username": username, "password": password})


def login_demo(client, username, password):
    return client.post('/login', json={"username": username, "password": password})


def create_category_demo(client, name):
    return client.post('/categories', json={"name": name})


def create_item_demo(client, token, name, description, category_id):
    return client.post('/items',
                       json={"name": name,
                             "description": description,
                             "category_id": category_id},
                       headers={"AUTHORIZATION": token}
                       )


def update_item_demo(client, token, item_id, name, description, category_id):
    return client.put('/items/' + str(item_id),
                      json={"name": name,
                             "description": description,
                             "category_id": category_id},
                      headers={"AUTHORIZATION": token}
                      )
