import logging
from flask import request, jsonify

from marshmallow import ValidationError

from app.security import requires_auth, get_user_id_from_request
from app.models.ItemModel import item_schema, ItemModel


def get_item(idx):
    """Response an item."""
    item = ItemModel.find_by_id(idx)
    if item:
        return item_schema.dump(item), 200
    return {'message': f'Item with id {idx} not found.'}, 400


@requires_auth
def create_item():
    """Create a new item, save to database and response it."""
    data = request.get_json()
    try:
        # add item's owner to data & validate request's data
        data['user_id'] = get_user_id_from_request()
        item = item_schema.load(data)

        # check if item's title has already existed
        if ItemModel.find_by_title(data.get('title')):
            return jsonify({'message': 'Title existed, please choose another title.'}), 400

        # save item to database and response
        item.save_to_db()
        return jsonify({
            'message': 'Successfully created item {}'.format(item.title),
            'item': item_schema.dump(item)
        }), 201
    except ValidationError as e:
        logging.exception("Invalid request data to create new item.")
        return jsonify(e.messages), 400
    except Exception as e:
        logging.exception("Unknown error.")
        return jsonify({'message': 'Unknown error.'}), 500


@requires_auth
def update_item(idx):
    """Update an existing item & response the updated one."""
    data = request.get_json()
    try:
        user_make_req = get_user_id_from_request()
        # check if the item exists
        item = ItemModel.find_by_id(idx)
        if item is None:
            return {'message': f'Item with id {idx} not found.'}, 400

        # check if the updater is the item's owner
        if item.user_id != user_make_req:
            return {'message': 'You are not the owner of this item.'}, 403

        # check if item's new title has already existed
        item_by_title = ItemModel.find_by_title(data.get('title'))

        if item_by_title and item_by_title.id != idx:
            return jsonify({'message': 'New title existed, please choose another title.'}), 400

        # validate item's data
        data['user_id'] = user_make_req
        item_schema.load(data)

        # updated item & response back to client
        item.update_to_db(data)
        return jsonify({
            'message': f'Successfully updated item id {idx}',
            'item': item_schema.dump(item)
        }), 200
    except ValidationError as e:
        logging.exception("Invalid request data to update this item.")
        return jsonify(e.messages), 400
    except Exception as e:
        logging.exception("Unknown error while updating an item.")
        return jsonify({'message': 'Unknown error while updating an item.'}), 500


@requires_auth
def delete_item(idx):
    # check if the item exists
    item = ItemModel.find_by_id(idx)
    if item is None:
        return {'message': f'Item with id {idx} not found.'}, 400

    # check if the updater is the item's owner
    if item.user_id != get_user_id_from_request():
        return {'message': 'You are not the owner of this item.'}, 403

    # delete the item & response a message
    try:
        item.delete_from_db()
        return {'message': f'Successfully deleted item with id {idx}.'}, 200
    except Exception as e:
        logging.exception("Unknown error while deleting an item.")
        return jsonify({'message': 'Unknown error while deleting an item.'}), 500
