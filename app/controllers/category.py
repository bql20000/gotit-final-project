import logging

from flask import jsonify, request
from marshmallow import ValidationError

from app.app import app
from app.models.category import CategoryModel
from app.schemas.item import ItemSchema
from app.schemas.category import CategorySchema


class CategoryNotFoundError(Exception):
    def __init__(self, messages='Category not found.', status_code=404):
        self.messages = messages
        self.status_code = status_code


def check_category_exists(idx):
    category = CategoryModel.query.filter_by(id=idx).first()
    if category is None:
        raise CategoryNotFoundError(f'Category with id {idx} not found.', 404)


@app.route('/categories', methods=['GET'])
def get_all_categories():
    """Return all categories"""
    try:
        all_cats = CategoryModel.query.all()
        return jsonify(categories=CategorySchema(many=True).dump(all_cats)), 200
    except:
        logging.exception('Unknown error while getting all categories.')
        return jsonify(message='Unknown error while getting all categories.'), 500


@app.route('/categories/<int:idx>', methods=['GET'])
def get_category_by_id(idx):
    """Return the category with id = idx."""
    try:
        check_category_exists(idx)
        category = CategoryModel.query.filter_by(id=idx).first()
        return jsonify(category=CategorySchema().dump(category)), 200
    except CategoryNotFoundError as e:
        return jsonify({'message': e.messages}), e.status_code
    except:
        logging.exception('Unknown error while getting a category.')
        return jsonify(message='Unknown error while getting a category.'), 500


@app.route('/categories', methods=['POST'])
def create_category():
    """Create a new category."""
    data = request.get_json()
    try:
        # validate the data
        CategorySchema().load(data)

        # check if new category's name has existed."
        if CategoryModel.query.filter_by(name=data.get('name')).first():
            return jsonify({'name': [f"Category {data.get('name')} existed."]}), 400

        # save category to database & response to client
        category = CategoryModel(**data)
        category.save_to_db()
        return jsonify(message=f'Successfully created category {category.name}.',
                       category=CategorySchema().dump(category)
                       ), 201
    except ValidationError as e:
        logging.exception('Invalid request data to create new category.')
        return jsonify(e.messages), 400
    except:
        logging.exception('Unknown error while creating new category.')
        return jsonify(message='Unknown error while creating new category.'), 500


@app.route('/categories/<int:idx>/items', methods=['GET'])
def get_all_items_in_category(idx):
    """Return all items in the category with id = idx."""
    # check if category with id = idx exists
    try:
        check_category_exists(idx)
        category = CategoryModel.query.filter_by(id=idx).first()
        n_items = len(category.items)
        n_items_per_page = 2
        n_pages = n_items // n_items_per_page + (n_items % n_items_per_page > 0)
        paginated_items = []
        for i in range(n_pages): paginated_items.append([])
        for i in range(n_items):
            i_page = i // n_items_per_page
            paginated_items[i_page].append(ItemSchema().dump(category.items[i]))

        return jsonify(number_of_items=n_items,
                       number_of_items_per_page=n_items_per_page,
                       number_of_pages=n_pages,
                       items=paginated_items), 200
    except CategoryNotFoundError as e:
        logging.exception(e.messages)
        return jsonify(message=e.messages), e.status_code
    except:
        logging.exception('Unknown error while getting all items in a category.')
        return jsonify(message='Unknown error while getting all items in a category.'), 500
