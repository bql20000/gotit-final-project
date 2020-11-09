from flask import Flask

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


app = create_app()

import main.controllers.user
import main.controllers.category
import main.controllers.item
import main.controllers.exception
