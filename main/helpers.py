from functools import wraps

from flask import request
from werkzeug.exceptions import NotFound, Forbidden

from main.models.category import CategoryModel
from main.models.item import ItemModel


def load_request_data(schema):
    """Deserialize a request data & validate it.

    :param schema: the schema used
    :return: deserialized data (dict)
    """

    def wrapper(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            if request.method == 'GET':
                data = schema().load(request.args)
            else:
                data = schema().load(request.get_json())
            return func(data=data, *args, **kwargs)
        return decorated_func
    return wrapper


def validate_ownership(item, user_id):
    """Check if item is owned by user with id = user_id."""
    if item.user_id != user_id:
        raise Forbidden('You are not allowed to modify this item.')


def validate_item_id(item_id):
    """Return the item object with id = {item_id} or None if not exist."""
    item = ItemModel.query.get(item_id)
    if item is None:
        raise NotFound(f'Item with id {item_id} not found.')
    return item


def validate_category_id(category_id):  #
    """Return the category object with id = {category_id} or None if not exist."""
    category = CategoryModel.query.get(category_id)
    if category is None:
        raise NotFound(f'Category with id {category_id} not found.')
    return category
