import logging
from werkzeug.exceptions import HTTPException

from flask import Flask, jsonify
from marshmallow import ValidationError

from main.extensions import db, hashing
from main.models.item import ItemModel
from main.models.user import UserModel
from main.models.category import CategoryModel


def register_extensions(app):
    """Register the application with needed extensions."""
    hashing.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()


def create_app():
    """Create a flask application & config environment"""
    app = Flask(__name__)

    if app.config['ENV'] == 'development':
        app.config.from_object('config.development.DevelopmentConfig')
    elif app.config['ENV'] == 'testing':
        app.config.from_object('config.testing.TestingConfig')
    else:
        raise Exception('Unknown environment.')

    register_extensions(app)

    return app


def init_routes():
    import main.controllers


app = create_app()
init_routes()


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all application's exceptions."""
    if isinstance(e, ValidationError):
        logging.exception(e)
        return jsonify(message='Invalid request data.', error_info=e.messages), 400

    if isinstance(e, HTTPException):
        logging.exception(e)
        return jsonify(message=e.description,
                       error_info=e.response.data if e.response else {}
                       ), e.code

    logging.exception(e)
    return jsonify(message='Internal server error.', error_info={}), 500


