from flask import Flask

from app.models.UserModel import UserModel
from app.controllers import user, item, category
from app.extensions import db


def create_app(env):
    app = Flask(__name__)

    if env == 'development':
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.TestingConfig')

    print('DATABASE URI:', app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)

    # user api
    app.add_url_rule('/register', view_func=user.register, methods=['POST'])
    app.add_url_rule('/login', view_func=user.login, methods=['POST'])

    # item api
    app.add_url_rule('/items/<int:idx>', view_func=item.get_item, methods=['GET'])
    app.add_url_rule('/items/new', view_func=item.create_item, methods=['POST'])
    app.add_url_rule('/items/<int:idx>', view_func=item.update_item, methods=['PUT'])
    app.add_url_rule('/items/<int:idx>', view_func=item.delete_item, methods=['DELETE'])

    # category api
    app.add_url_rule('/categories', view_func=category.get_all_categories)
    app.add_url_rule('/categories/<int:idx>', view_func=category.get_category_by_id)
    app.add_url_rule('/categories/new', view_func=category.create_category, methods=['POST'])
    app.add_url_rule('/categories/<int:idx>/items', view_func=category.get_all_items_in_category)

    return app
