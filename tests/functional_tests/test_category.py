from app.models.category import CategoryModel


def create_two_sample_categories(client, name1, name2):
    create_category_demo(client, name1)
    create_category_demo(client, name2)


def create_category_demo(client, name):
    return client.post('/categories', json={"name": name})


def test_create_category(init_client, init_db):
    """Create a new category & test duplicated name."""

    test_cat_name = 'soccer'
    # successful
    resp = create_category_demo(init_client, test_cat_name)
    assert resp.status_code == 201
    assert resp.get_json().get('message') == f'Successfully created category {test_cat_name}.'

    # category name existed
    resp = create_category_demo(init_client, test_cat_name)
    assert resp.status_code == 400
    assert resp.get_json().get('message') == f'Category {test_cat_name} existed.'


def test_get_all_categories(init_client, init_db):
    """Test get all categories in database."""
    create_two_sample_categories(init_client, 'soccer', 'badminton')

    resp = init_client.get('/categories')
    number_of_categories = len(CategoryModel.query.all())
    assert resp.status_code == 200
    assert len(resp.get_json()) == number_of_categories


def test_get_category_by_id(init_client, init_db):
    """Test get a category by its id."""
    create_two_sample_categories(init_client, 'soccer', 'badminton')
    test_id = 1

    resp = init_client.get('/categories/' + str(test_id))
    assert resp.status_code == 200
    assert resp.get_json().get('name') == 'soccer'
    assert resp.get_json().get('id') == test_id


def test_get_all_items_in_category_by_id(init_client, init_db):
    pass

