import pytest

from app.users.dao import UsersDAO


@pytest.mark.parametrize('user_id, email, is_exist', [
    (1, 'test@test.com', True),
    (2, 'artem@example.com', True),
    (3, 'asbcz', False)
])
async def test_find_by_id(user_id, email, is_exist):
    user = await UsersDAO.find_by_id(user_id)

    if is_exist:
        assert user
        assert user_id == user_id
        assert user.email == email
    else:
        assert not user
