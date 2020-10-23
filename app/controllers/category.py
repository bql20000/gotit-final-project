import logging
from flask import jsonify, request
from marshmallow import ValidationError

from app.models.CategoryModel import CategoryModel, category_schema


def get_all_categories():
    all_cats = CategoryModel.query.all()
    return jsonify(category_schema.dump(all_cats, many=True)), 200


def get_category_by_id(idx):
    cat = CategoryModel.query.filter_by(id=idx).first()
    if cat:
        return jsonify(category_schema.dump(cat)), 200
    return jsonify({'message': 'Category not found.'}), 404


def create_category():
    data = request.get_json()
    try:
        cat = category_schema.load(data)
        if CategoryModel.find_by_name(data.get('name')):
            return jsonify({'message': 'Category existed.'}), 400
        cat.save_to_db()
        return jsonify({
            'status': 'success',
            'message': 'Successfully created category {}'.format(cat.name),
            'category': category_schema.dump(cat)
        })
    except ValidationError as err:
        logging.exception("Invalid category name: {}.".format(data.get('name')))
        return jsonify(err.messages), 400


def get_all_items_in_category(idx):
    pass
