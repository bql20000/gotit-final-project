from flask import Flask

from app.extensions import db, hashing
from app.models.item import ItemModel
from app.models.user import UserModel
from app.models.category import CategoryModel


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

    # print("DATABASE:", app.config['SQLALCHEMY_DATABASE_URI'])

    register_extensions(app)

    return app
