from flask import request, jsonify
from marshmallow import ValidationError

from app.models.UserModel import UserModel, user_schema
from app.database import db


def register():
    """
        Docs ...
    """
    data = request.get_json()
    if UserModel.find_by_username(data['username']):
        return jsonify({'message': 'Username existed, please choose another username.'}), 400
    try:
        user = user_schema.load(data)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registers successfully!'}), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

