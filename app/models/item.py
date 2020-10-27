from app.extensions import db


class ItemModel(db.Model):
    """The item model"""

    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    description = db.Column(db.String(255))

    # items table has 2 foreign keys referencing users & categories table
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # category = db.relationship('CategoryModel')
    # user = db.relationship('UserModel')

    def __init__(self, name, description, category_id, user_id):
        self.name = name
        self.description = description
        self.category_id = category_id
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_to_db(self, data):
        self.query.filter_by(id=self.id).update(data)
        db.session.commit()
