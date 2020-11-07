from flask import Flask

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
        app.config.from_object('config.development.DevelopmentConfig')
    elif app.config['ENV'] == 'testing':
        app.config.from_object('config.testing.TestingConfig')
    else:
        raise Exception('Unknown environment.')

    register_extensions(app)

    return app


app = create_app()

import flaskr.controllers.user
import flaskr.controllers.category
import flaskr.controllers.item
import flaskr.controllers.exception
