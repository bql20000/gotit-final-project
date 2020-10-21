from app.models.UserModel import UserModel


def get_user():
    return UserModel.query.filter_by(username='aaa').first().json()