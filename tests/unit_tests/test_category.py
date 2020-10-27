from app.models.CategoryModel import CategoryModel


def test_initialization(init_client, init_db):
    test_cat_name = 'soccer'
    new_cat = CategoryModel(test_cat_name)
    new_cat.save_to_db()
    cat = CategoryModel.find_by_name(test_cat_name)
    assert cat.name == test_cat_name

