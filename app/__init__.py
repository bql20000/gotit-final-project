from flask import Flask

from app.models.UserModel import UserModel
from app.controllers import user, item
from app.extensions import db


def create_app():
    app = Flask(__name__)

    if app.config['ENV'] == 'development':
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.TestingConfig')

    print('DATABASE URI:', app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.add_url_rule('/register', view_func=user.register, methods=['POST'])
    app.add_url_rule('/login', view_func=user.login, methods=['POST'])

    app.add_url_rule('/', view_func=item.get_item, methods=['GET'])
    app.add_url_rule('/items/new', view_func=item.create_item, methods=['POST'])

    return app
