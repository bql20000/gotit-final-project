from marshmallow.validate import Validator
from marshmallow import ValidationError

from flaskr.models.category import CategoryModel


class FirstCharNotNum(Validator):
    error = 'First character must not be a number.'

    def __call__(self, value):
        if value and '9' >= value[0] >= '0':
            raise ValidationError(FirstCharNotNum.error)
        return value


class CategoryExists(Validator):
    error = 'Category with id {category_id} not found.'

    def __call__(self, category_id):
        if CategoryModel.query.get(category_id) is None:
            raise ValidationError(self.error.format(category_id))
        return category_id
