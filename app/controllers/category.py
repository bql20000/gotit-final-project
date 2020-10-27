import logging

from flask import jsonify, request
from marshmallow import ValidationError

from app.models.category import CategoryModel
from app.schemas.item import item_schema
from app.schemas.category import category_schema


def get_all_categories():
    """Return all categories"""
    all_cats = CategoryModel.query.all()
    return jsonify(category_schema.dump(all_cats, many=True)), 200


def get_category_by_id(idx):
    """Return the category with id = idx."""
    category = CategoryModel.query.filter_by(id=idx).first()
    if category:
        return jsonify(category_schema.dump(category)), 200
    return jsonify({'message': 'Category not found.'}), 404


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
    category = CategoryModel.query.filter_by(id=idx).first()
    if category is None:
        return {'message': f'Category with id {idx} not found.'}, 400
    return jsonify({'items': [item_schema.dump(item) for item in category.items]}), 200
