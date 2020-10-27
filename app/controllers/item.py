import logging
from flask import request, jsonify

from marshmallow import ValidationError

from app.security import requires_auth
from app.schemas.item import item_schema
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


def get_item(idx):
    """Response an item."""
    try:
        check_item_exists_by_id(idx)
        item = ItemModel.find_by_id(idx)
        return item_schema.dump(item), 200
    except ItemNotFoundError as e:
        logging.exception(e.messages)
        return jsonify({'messages': e.messages}), e.status_code
    except:
        logging.exception('Unknown error while getting an item.')
        return jsonify({'message': 'Unknown error while getting an item.'}), 500


@requires_auth
def create_item(user_id):
    """Create a new item, save to database and response it."""
    data = request.get_json()
    try:
        # add item's owner to data & validate request's data
        item_schema.load(data)

        # check if item's title has already existed
        if ItemModel.query.filter_by(name=data.get('name')).first():
            raise ValidationError('Title existed, please choose another title.')

        # save item to database and response
        item = ItemModel(**data, user_id=user_id)
        item.save_to_db()
        return jsonify({
            'message': f'Successfully created item {item.name}.',
            'item': item_schema.dump(item)
        }), 201
    except (OwnershipError, ItemNotFoundError) as e:
        logging.exception(e.messages)
        return jsonify({'messages': e.messages}), e.status_code
    except ValidationError as e:
        logging.exception('Invalid request data to create new item.')
        return jsonify({'messages': e.messages}), 400
    except:
        logging.exception('Unknown error.')
        return jsonify({'message': 'Unknown error.'}), 500


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
            raise ValidationError('New item name existed.', status_code=400)

        # validate item's data
        item_schema.load(data)

        # updated item & response back to client
        ItemModel.query.filter_by(id=idx).update(data)
        db.session.commit()

        return jsonify({
            'message': f'Successfully updated item id {idx}.',
            'item': item_schema.dump(ItemModel.query.filter_by(id=idx).first())
        }), 200
    except (OwnershipError, ItemNotFoundError) as e:
        logging.exception(e.messages)
        return jsonify({'messages': e.messages}), e.status_code
    except ValidationError as e:
        logging.exception('Invalid request data to create new item.')
        return jsonify({'messages': e.messages}), 400
    except:
        logging.exception('Unknown error while updating an item.')
        return jsonify({'message': 'Unknown error while updating an item.'}), 500


@requires_auth
def delete_item(idx, user_id):
    # check if the item exists
    check_item_exists_by_id(idx)

    # check if the deleter is the item's owner
    check_item_ownership(idx, user_id)

    # delete the item & response a message
    try:
        item = ItemModel.query.filter_by(id=idx).first()
        item.delete_from_db()
        return jsonify({'message': f'Successfully deleted item with id {idx}.'}), 200
    except (OwnershipError, ItemNotFoundError) as e:
        logging.exception(e.messages)
        return jsonify({'messages': e.messages}), e.status_code
    except:
        logging.exception('Unknown error while deleting an item.')
        return jsonify({'message': 'Unknown error while deleting an item.'}), 500
