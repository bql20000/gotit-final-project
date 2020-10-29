from app.models.category import CategoryModel
from tests.helpers import create_category_demo

def test_create_category(init_client, init_db):
    """Create a new category & test duplicated name."""

    test_name = 'a' * 32
    # successful & category name = 32
    resp = create_category_demo(init_client, test_name)
    assert resp.status_code == 201
    assert resp.get_json()['id'] == 3      # after 2 sample categories
    assert resp.get_json()['name'] == test_name

    # category name existed
    resp = create_category_demo(init_client, test_name)
    assert resp.status_code == 400
    assert resp.get_json()['message'] == f'Category {test_name} existed.'

    # category name length = 0
    test_name = ""
    resp = create_category_demo(init_client, test_name)
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Invalid request data.'
    assert resp.get_json()['error_info']['name'][0] == 'Length must be between 1 and 32.'

    # category name length > 32
    test_name = 'a' * 33
    resp = create_category_demo(init_client, test_name)
    assert resp.status_code == 400
    assert resp.get_json()['message'] == 'Invalid request data.'
    assert resp.get_json()['error_info']['name'][0] == 'Length must be between 1 and 32.'


def test_get_all_categories(init_client, init_db):
    """Test get all categories in database."""

    resp = init_client.get('/categories')
    number_of_categories = len(CategoryModel.query.all())
    assert resp.status_code == 200
    assert len(resp.get_json()) == number_of_categories


def test_get_category_by_id(init_client, init_db):
    """Test get a category by its id."""

    test_id = 1
    resp = init_client.get('/categories/' + str(test_id))
    assert resp.status_code == 200
    assert resp.get_json()['name'] == 'soccer'
    assert resp.get_json()['id'] == test_id

    test_id = 0
    resp = init_client.get('/categories/' + str(test_id))
    assert resp.status_code == 404
    assert resp.get_json()['message'] == f'Category with id {test_id} not found.'


def test_get_all_items_in_category_by_id(init_client, init_db):
    pass

