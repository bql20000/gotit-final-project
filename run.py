from app import create_app
from app.database import db

from app.models.UserModel import UserModel
from flask import jsonify

app = create_app()
db.init_app(app)


@app.route('/')
def home():
    return "HOME PAGE"


@app.route('/register', methods=['POST', 'GET'])
def register():
    user = UserModel('long', 'asdf')
    db.session.add(user)
    db.session.commit()
    return jsonify(username=user.username)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
