import logging

from flask import jsonify, request
from marshmallow import ValidationError

from app.models.category import CategoryModel
from app.schemas.item import item_schema
from app.schemas.category import category_schema


class CategoryNotFoundError(Exception):
    def __init__(self, messages='Category not found.', status_code=404):
        self.messages = messages
        self.status_code = status_code


def check_category_exists(idx):
    category = CategoryModel.query.filter_by(id=idx).first()
    if category is None:
        raise CategoryNotFoundError(f'Category with id {idx} not found.', 404)


def get_all_categories():
    """Return all categories"""
    all_cats = CategoryModel.query.all()
    return jsonify(category_schema.dump(all_cats, many=True)), 200


def get_category_by_id(idx):
    """Return the category with id = idx."""
    try:
        check_category_exists(idx)
        category = CategoryModel.query.filter_by(id=idx).first()
        return jsonify(category_schema.dump(category)), 200
    except CategoryNotFoundError as e:
        return jsonify({'message': e.messages}), e.status_code


def create_category():
    """Create a new category."""
    data = request.get_json()
    try:
        # validate the data
        category_schema.load(data)

        # check if new category's name has existed."
        if CategoryModel.query.filter_by(name=data.get('name')).first():
            return jsonify({'message': f"Category {data.get('name')} existed."}), 400

        # save category to database & response to client
        category = CategoryModel(**data)
        category.save_to_db()
        return jsonify({
            'message': f'Successfully created category {category.name}.',
            'category': category_schema.dump(category)
        }), 201
    except ValidationError as e:
        logging.exception('Invalid request data to create new category.')
        return jsonify({'messages': e.messages}), 400
    except Exception as e:
        logging.exception('Unknown error while creating new category.')
        return jsonify({'message': 'Unknown error while creating new category.'}), 500


def get_all_items_in_category(idx):
    """Return all items in the category with id = idx."""
    # check if category with id = idx exists
    try:
        check_category_exists(idx)
        category = CategoryModel.query.filter_by(id=idx).first()
        return jsonify({'items': [item_schema.dump(item) for item in category.items]}), 200
    except CategoryNotFoundError as e:
        logging.exception(e.messages)
        return jsonify({'message': e.messages}), e.status_code
    except:
        logging.exception('Unknown error while getting all items in a category.')
        return jsonify(message='Unknown error while creating new category.'), 500

