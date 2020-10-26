from flask import request, jsonify

from marshmallow import ValidationError

from app.security import requires_auth, get_user_id_from_request
from app.models.ItemModel import item_schema, ItemModel


@requires_auth
def get_item():
    return "Long dep trai"


@requires_auth
def create_item():
    """ Create a new item and save to database """
    data = request.get_json()
    try:
        # todo: write validation to check title exists & valid category
        data['user_id'] = get_user_id_from_request()
        item = item_schema.load(data)
        if ItemModel.find_by_title(data.get('title')):
            return jsonify({'message': 'Title existed, please choose another title.'}), 400
        item.save_to_db()
    except ValidationError as e:
        return jsonify(e.messages), 400


