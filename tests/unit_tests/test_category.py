from app.models.category import CategoryModel


def test_initialization(init_client, init_db):
    test_cat_name = 'soccer'
    new_cat = CategoryModel(test_cat_name)
    new_cat.save_to_db()
    cat = CategoryModel.query.filter_by(name=test_cat_name).first()
    assert cat.name == test_cat_name

