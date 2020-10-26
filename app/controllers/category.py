import logging

from flask import jsonify, request
from marshmallow import ValidationError

from app.models.CategoryModel import CategoryModel, category_schema
from app.models.ItemModel import item_schema


def get_all_categories():
    """Return all categories"""
    all_cats = CategoryModel.query.all()
    return jsonify(category_schema.dump(all_cats, many=True)), 200


def get_category_by_id(idx):
    """Return the category with id = idx."""
    cat = CategoryModel.query.filter_by(id=idx).first()
    if cat:
        return jsonify(category_schema.dump(cat)), 200
    return jsonify({'message': 'Category not found.'}), 404


def create_category():
    """Create a new category."""
    data = request.get_json()
    try:
        # validate the data
        cat = category_schema.load(data)

        # check if new category's name has existed."
        if CategoryModel.find_by_name(data.get('name')):
            return jsonify({'message': f"Category {data.get('name')} existed."}), 400

        # save category to database & response to client
        cat.save_to_db()
        return jsonify({
            'message': 'Successfully created category {}'.format(cat.name),
            'category': category_schema.dump(cat)
        }), 201
    except ValidationError as e:
        logging.exception('Invalid request data to create new category.')
        return jsonify(e.messages), 400
    except Exception as e:
        logging.exception('Unknown error while creating new category.')
        return jsonify({'message': 'Unknown error while creating new category.'}), 500


def get_all_items_in_category(idx):
    """Return all items in the category with id = idx."""
    # check if category with id = idx exists
    cat = CategoryModel.find_by_id(idx)
    if cat is None:
        return {'message': f'Category with id {idx} not found.'}, 400
    return jsonify({'items': [item_schema.dump(item) for item in cat.items]}), 200
