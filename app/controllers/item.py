import logging
from flask import request, jsonify

from marshmallow import ValidationError

from app.app import app
from app.security import requires_auth
from app.schemas.item import ItemSchema
from app.models.item import ItemModel
from app.extensions import db


class ItemNotFoundError(Exception):
    def __init__(self, messages='Item not found.', status_code=404):
        self.messages = messages
        self.status_code = status_code


class OwnershipError(Exception):
    def __init__(self, messages='Ownership required.', status_code=403):
        self.messages = messages
        self.status_code = status_code


def check_item_exists_by_id(idx):
    """Raise an exception if item with id=idx does not exist."""
    item = ItemModel.query.filter_by(id=idx).first()
    if item is None:
        raise ItemNotFoundError(f'Item with id {idx} not found.')


def check_item_ownership(idx, user_id):
    """Raise an exception if user with id=idx doesn't own item with id=idx"""
    if ItemModel.query.filter_by(id=idx).first().user_id != user_id:
        raise OwnershipError(f'You are not the owner of item with id {idx}.')


@app.route('/items/<int:idx>', methods=['GET'])
def get_item(idx):
    """Response an item with id = idx."""
    try:
        check_item_exists_by_id(idx)
        item = ItemModel.query.filter_by(id=idx).first()
        return jsonify(item=ItemSchema().dump(item)), 200
    except ItemNotFoundError as e:
        logging.exception(e.messages)
        return jsonify(message=e.messages), e.status_code
    except:
        logging.exception('Unknown error while getting an item.')
        return jsonify(message='Unknown error while getting an item.'), 500


@app.route('/items', methods=['POST'])
@requires_auth
def create_item(user_id):
    """Create a new item, save to database and response it."""
    data = request.get_json()
    try:
        # add item's owner to data & validate request's data
        ItemSchema().load(data)

        # check if item's title has already existed
        if ItemModel.query.filter_by(name=data.get('name')).first():
            raise ValidationError({'name': ['Title existed, please choose another title.']})

        # save item to database and response
        item = ItemModel(**data, user_id=user_id)
        item.save_to_db()
        return jsonify(message=f'Successfully created item {item.name}.',
                       item=ItemSchema().dump(item)
                       ), 201
    except ValidationError as e:
        logging.exception('Invalid request data to create new item.')
        response = {'name': [], 'description': [], 'category_id': []}
        if e.messages.get('name'):
            response['name'] = e.messages.get('name')
        if e.messages.get('description'):
            response['description'] = e.messages.get('description')
        if e.messages.get('category_id'):
            response['category_id'] = e.messages.get('category_id')
        return jsonify(response), 400
    except:
        logging.exception('Unknown error while creating a new item.')
        return jsonify(message='Unknown error while creating a new item.'), 500


@app.route('/items/<int:idx>', methods=['PUT'])
@requires_auth
def update_item(idx, user_id):
    """Update an existing item & response the updated one."""
    data = request.get_json()
    try:
        # check if the item exists
        check_item_exists_by_id(idx)

        # check if the updater is the item's owner
        check_item_ownership(idx, user_id)

        # check if item's new title has already existed
        item_by_name = ItemModel.query.filter_by(name=data.get('name')).first()
        if item_by_name and item_by_name.id != idx:
            raise ValidationError({'name': ['New item name existed.']})

        # validate item's data
        ItemSchema().load(data)

        # updated item & response back to client
        ItemModel.query.filter_by(id=idx).update(data)
        db.session.commit()

        return jsonify(message=f'Successfully updated item with id {idx}.',
                       item=ItemSchema().dump(ItemModel.query.filter_by(id=idx).first())
                       ), 200
    except (OwnershipError, ItemNotFoundError) as e:
        logging.exception(e.messages)
        return jsonify(message=e.messages), e.status_code
    except ValidationError as e:
        logging.exception('Invalid request data to update item.')
        response = {'name': [], 'description': [], 'category_id': []}
        if e.messages.get('name'):
            response['name'] = e.messages.get('name')
        if e.messages.get('description'):
            response['description'] = e.messages.get('description')
        if e.messages.get('category_id'):
            response['category_id'] = e.messages.get('category_id')
        return jsonify(response), 400
    except:
        logging.exception('Unknown error while updating an item.')
        return jsonify(message='Unknown error while updating an item.'), 500


@app.route('/items/<int:idx>', methods=['DELETE'])
@requires_auth
def delete_item(idx, user_id):
    try:
        # check if the item exists
        check_item_exists_by_id(idx)

        # check if the deleter is the item's owner
        check_item_ownership(idx, user_id)

        # delete the item & response a message
        item = ItemModel.query.filter_by(id=idx).first()
        item.delete_from_db()
        return jsonify(message=f'Successfully deleted item with id {idx}.'), 200
    except (OwnershipError, ItemNotFoundError) as e:
        logging.exception(e.messages)
        return jsonify(message=e.messages), e.status_code
    except:
        logging.exception('Unknown error while deleting an item.')
        return jsonify(message='Unknown error while deleting an item.'), 500
