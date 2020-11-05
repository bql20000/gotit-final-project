from flaskr.extensions import db
from flaskr.models.timestamp_mixin import TimestampMixin


class CategoryModel(db.Model, TimestampMixin):
    """The category model"""

    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    items = db.relationship('ItemModel')  #

    def __init__(self, name):
        self.name = name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
