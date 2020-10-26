from app.models.UserModel import UserModel


def test_initialization(init_client, init_db):
    new_user = UserModel('bill', '1234')
    new_user.save_to_db()
    user = UserModel.find_by_username('bill')
    assert user.id == 3
    assert user.username == 'bill'
    assert user.password == '1234'
