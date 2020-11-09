import logging
from werkzeug.exceptions import HTTPException

from flask import Flask, jsonify
from marshmallow import ValidationError

from main.extensions import db, hashing


def create_app():
    """Create a flask application & config environment"""
    app = Flask(__name__)
    try:
        app.config.from_object(f'config.{app.config["ENV"]}.config')
    except:
        raise Exception(f'Unknown environment {app.config["ENV"]}.')

    return app


def register_controllers_and_models():
    import main.controllers
    import main.models


def register_extensions():
    """Register the application with needed extensions."""
    hashing.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()


app = create_app()
register_controllers_and_models()
register_extensions()


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
