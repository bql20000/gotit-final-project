from app.database import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {'username': self.username}

    @classmethod
    def find_by_username(cls):
        pass

    @classmethod
    def find_by_id(cls):
        pass