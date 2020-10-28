from flask import jsonify
from werkzeug.exceptions import BadRequest

from app.app import app
from app.models.category import CategoryModel
from app.schemas.item import ItemSchema
from app.schemas.page import PageSchema
from app.schemas.category import CategorySchema
from app.helpers import validate_category_id, load_request_data


@app.route('/categories', methods=['GET'])
def get_all_categories():
    """Return all categories"""
    all_cats = CategoryModel.query.all()
    return jsonify(CategorySchema(many=True).dump(all_cats)), 200


@app.route('/categories/<int:idx>', methods=['GET'])
def get_category_by_id(idx):
    """Return the category with id = idx."""
    category = validate_category_id(idx)
    return jsonify(CategorySchema().dump(category)), 200


@app.route('/categories', methods=['POST'])
@load_request_data(CategorySchema)
def create_category(data):
    """Create a new category."""

    # check if new category's name has existed."
    if CategoryModel.query.filter_by(name=data.get('name')).first():
        raise BadRequest(f"Category {data.get('name')} existed.")

    # save category to database & response to client
    category = CategoryModel(**data)
    category.save_to_db()
    return jsonify(CategorySchema().dump(category)), 201


@app.route('/categories/<int:idx>/items', methods=['POST'])
@load_request_data(PageSchema)
def get_all_items_in_category(idx, data):
    """ Return all items in 1 page of the category with id = idx.

    The item page is specified by 2 fields in the post request:
        page_number (default=1): the wanted page
        items_per_page (default=2): the items in each page
    """

    # set params as default if not provided
    page_number = data.get('page_number') if data.get('page_number') else 1
    items_per_page = data.get('items_per_page') if data.get('items_per_page') else 2

    # check if category with id = idx exists
    category = validate_category_id(idx)

    total_items = len(category.items)
    total_pages = total_items // items_per_page + (total_items % items_per_page > 0)
    first_item_number = items_per_page * (page_number - 1)
    last_item_number = items_per_page * page_number     # exclusive

    return jsonify(total_items=total_items,
                   current_page=page_number,
                   items_per_page=items_per_page,
                   total_pages=total_pages,
                   items=ItemSchema(many=True).dump(category.items[first_item_number:last_item_number])), 200
