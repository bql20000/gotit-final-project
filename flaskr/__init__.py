import logging

from flask import Flask, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from flaskr.extensions import db, hashing
from flaskr.models.item import ItemModel
from flaskr.models.user import UserModel
from flaskr.models.category import CategoryModel


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
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.TestingConfig')

    register_extensions(app)

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle all application's exceptions."""
        if isinstance(e, ValidationError):
            logging.exception(e)
            return jsonify(message='Invalid request data.', error_info=e.messages), 400  #

        if isinstance(e, HTTPException):
            logging.exception(e)
            return jsonify(message=e.description,
                           error_info=e.response.data if e.response else {}
                           ), e.code

        logging.exception(e)
        return jsonify(message='Internal Server Error.'), 500

    return app


app = create_app()

import flaskr.controllers.user
import flaskr.controllers.category
import flaskr.controllers.item

