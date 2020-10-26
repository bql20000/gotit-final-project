from app.models.UserModel import UserModel


def test_register(init_client, init_db):
    new_user = UserModel('bill', '1234')
    new_user.save_to_db()
    # return
    # user = UserModel.find_by_username('bill')
    user = new_user
    assert user.id != 3
    assert user.username == 'bill'
    assert user.password == '1234'