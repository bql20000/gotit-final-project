from flask import Flask

from app.models.UserModel import UserModel
from app.controllers import user
from app.database import db


def create_app():
    app = Flask(__name__)

    if app.config['ENV'] == 'development':
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.TestingConfig')

    print('DATABASE URI:', app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)

    app.add_url_rule('/register', view_func=user.register, methods=['POST'])

    return app
