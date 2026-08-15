import pytest

from exceptions.user_exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from models.user import User


def test_service_get_all_users(user_service):
    user1 = User(username="Ali")
    user2 = User(username="Reza")

    user_service.create(user1)
    user_service.create(user2)

    result = user_service.get_all()

    usernames = sorted(user.username for user in result)

    assert usernames == ["Ali", "Reza"]


def test_service_get_user_by_id_success(user_service):
    user = User(username="Ali")

    user_service.create(user)

    result = user_service.get_by_id(user.user_id)

    assert result.user_id == user.user_id
    assert result.username == "Ali"


def test_service_get_user_by_id_not_found(user_service):
    with pytest.raises(UserNotFoundException):
        user_service.get_by_id(9999)


def test_service_create_user(user_service):
    user = User(username="Ali")

    result = user_service.create(user)

    assert result.user_id is not None
    assert result.username == "Ali"


def test_service_create_user_duplicate(user_service):
    user1 = User(username="Ali")
    user2 = User(username="Ali")

    user_service.create(user1)

    with pytest.raises(UserAlreadyExistsException):
        user_service.create(user2)


def test_service_update_user_success(user_service):
    user = User(username="Ali")

    user_service.create(user)

    updated_user = User(username="Reza")

    result = user_service.update(
        user.user_id,
        updated_user,
    )

    assert result.user_id == user.user_id
    assert result.username == "Reza"


def test_service_update_user_not_found(user_service):
    updated_user = User(username="Reza")

    with pytest.raises(UserNotFoundException):
        user_service.update(
            9999,
            updated_user,
        )


def test_service_delete_user_success(user_service):
    user = User(username="Ali")

    user_service.create(user)

    deleted_user = user_service.delete(user.user_id)

    assert deleted_user.user_id == user.user_id
    assert deleted_user.username == "Ali"

    with pytest.raises(UserNotFoundException):
        user_service.get_by_id(user.user_id)


def test_service_delete_user_not_found(user_service):
    with pytest.raises(UserNotFoundException):
        user_service.delete(9999)