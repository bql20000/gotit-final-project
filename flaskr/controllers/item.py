from flask import jsonify
from werkzeug.exceptions import BadRequest

from flaskr import app
from flaskr.security import requires_auth
from flaskr.schemas.item import ItemSchema
from flaskr.models.item import ItemModel
from flaskr.extensions import db
from flaskr.helpers import validate_item_id, load_request_data, validate_ownership


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Response an item with id = item_id."""
    item = validate_item_id(item_id)
    return jsonify(ItemSchema().dump(item)), 200


@app.route('/items', methods=['POST'])
@requires_auth
@load_request_data(ItemSchema)
def create_item(data, user_id):
    """Create a new item, save to database and response it."""

    # check if item's name has already existed in this category
    if ItemModel.query.filter_by(name=data['name'],
                                 category_id=data['category_id']
                                 ).first():
        raise BadRequest(f"This category has already had item {data['name']}.")

    # save item to database and response
    item = ItemModel(**data, user_id=user_id)
    item.save_to_db()
    return jsonify(ItemSchema().dump(item)), 201


@app.route('/items/<int:item_id>', methods=['PUT'])
@requires_auth
@load_request_data(ItemSchema)
def update_item(item_id, data, user_id):
    """Update an existing item & response the updated one."""

    # check if the item exists
    item = validate_item_id(item_id)

    # check if the updater is the item's owner
    validate_ownership(item, user_id)

    # check if item's new name has already existed in this category
    existed_item = ItemModel.query.filter_by(name=data['name'],
                                             category_id=data['category_id']
                                             ).first()
    if existed_item and existed_item.id != item_id:
        raise BadRequest(f"This category has already had item {data['name']}.")

    # updated item & response back to client
    item.name = data['name']
    item.description = data['description']
    item.category_id = data['category_id']
    db.session.commit()

    return jsonify(ItemSchema().dump(item)), 200


@app.route('/items/<int:item_id>', methods=['DELETE'])
@requires_auth
def delete_item(item_id, user_id):
    """Delete an item from database."""
    # check if the item exists
    item = validate_item_id(item_id)

    # check if the deleter is the item's owner
    validate_ownership(item, user_id)

    # delete the item & response a message
    item.delete_from_db()
    return jsonify({}), 200
