from flask import jsonify
from werkzeug.exceptions import BadRequest

from main import app
from main.models.category import CategoryModel
from main.schemas.item import ItemSchema
from main.schemas.page import PageSchema
from main.schemas.category import CategorySchema
from main.helpers import validate_category_id, load_request_data


@app.route('/categories', methods=['GET'])
def get_all_categories():
    """Return all categories"""
    all_cats = CategoryModel.query.all()
    return jsonify(CategorySchema(many=True).dump(all_cats)), 200


@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    """Return the category with id = category_id."""
    category = validate_category_id(category_id)
    return jsonify(CategorySchema().dump(category)), 200


@app.route('/categories', methods=['POST'])
@load_request_data(CategorySchema)
def create_category(data):
    """Create a new category."""

    # check if new category's name has existed."
    if CategoryModel.query.filter_by(name=data['name']).first():
        raise BadRequest(f"Category {data['name']} existed.")

    # save category to database & response to client
    category = CategoryModel(**data)
    category.save_to_db()
    return jsonify(CategorySchema().dump(category)), 201


@app.route('/categories/<int:category_id>/items', methods=['GET'])
@load_request_data(PageSchema)
def get_items_in_category(category_id, data):
    """ Return all items in 1 page of the category with id = category_id.

    The item page is specified by 2 fields in the post request:
        page_number (default=1): the wanted page
        items_per_page (default=2): the items in each page
    """

    # check if category with id = category_id exists
    category = validate_category_id(category_id)

    # set params as default if not provided
    page_number = int(data.get('page_number', 1))
    items_per_page = int(data.get('items_per_page', 2))

    result_page = category.items.paginate(page_number, items_per_page, False)

    return jsonify(total_items=result_page.total,
                   current_page=page_number,
                   items_per_page=items_per_page,
                   total_pages=result_page.pages,
                   items=ItemSchema(many=True).dump(result_page.items)), 200
