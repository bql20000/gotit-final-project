from flask import jsonify
from werkzeug.exceptions import BadRequest

from app.app import app
from app.security import requires_auth
from app.schemas.item import ItemSchema
from app.models.item import ItemModel
from app.extensions import db
from app.helpers import validate_item_id, load_request_data, validate_ownership


@app.route('/items/<int:idx>', methods=['GET'])
def get_item(idx):
    """Response an item with id = idx."""
    item = validate_item_id(idx)
    return jsonify(ItemSchema().dump(item)), 200


@app.route('/items', methods=['POST'])
@requires_auth
@load_request_data(ItemSchema)
def create_item(data, user_id):
    """Create a new item, save to database and response it."""

    # check if item's title has already existed
    if ItemModel.query.filter_by(name=data['name']).first():
        raise BadRequest(f"Item {data['name']} existed.")

    # save item to database and response
    item = ItemModel(**data, user_id=user_id)
    item.save_to_db()
    return jsonify(ItemSchema().dump(item)), 201


@app.route('/items/<int:idx>', methods=['PUT'])
@requires_auth
@load_request_data(ItemSchema)
def update_item(idx, data, user_id):
    """Update an existing item & response the updated one."""

    # check if the item exists
    item = validate_item_id(idx)

    # check if the updater is the item's owner
    validate_ownership(item, user_id)

    # check if item's new title has already existed
    item_by_name = ItemModel.query.filter_by(name=data['name']).first()
    if item_by_name and item_by_name.id != idx:
        raise BadRequest(f"Item {data['name']} existed.")

    # updated item & response back to client
    ItemModel.query.filter_by(id=idx).update(data)
    db.session.commit()

    return jsonify(ItemSchema().dump(item)), 200


@app.route('/items/<int:idx>', methods=['DELETE'])
@requires_auth
def delete_item(idx, user_id):
    """Delete an item from database."""
    # check if the item exists
    item = validate_item_id(idx)

    # check if the deleter is the item's owner
    validate_ownership(item, user_id)

    # delete the item & response a message
    item.delete_from_db()
    return jsonify({}), 200

