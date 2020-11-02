import typing

from marshmallow.validate import Validator
from marshmallow import ValidationError

from app.models.category import CategoryModel


class FirstCharNotNum(Validator):
    error = 'First character must not be a number.'

    def __call__(self, value) -> typing.Any:
        if value and '9' >= value[0] >= '0':
            raise ValidationError(FirstCharNotNum.error)
        return value


class CategoryExists(Validator):
    error = 'Category with id {idx} not found.'

    def __call__(self, category_id) -> typing.Any:
        category = CategoryModel.query.filter_by(id=category_id).first()
        if category is None:
            raise ValidationError(self.error.format(idx=category_id))
