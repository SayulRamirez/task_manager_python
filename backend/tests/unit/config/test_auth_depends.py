import pytest
from unittest.mock import MagicMock, patch
from models.user import Role, User
from exceptions.auth import ForbiddenException, UnauthorizedUser
from config.auth_depends import get_current_user, RoleChecker


# --- Pruebas de get_current_user ---

@patch("config.auth_depends.JWTManager.decode_token")
def test_get_current_user_success(mock_decode):
    mock_decode.return_value = {"id": 1}
    mock_repo = MagicMock()
    expected_user = User(id=1, is_active=True)
    mock_repo.find_by_id.return_value = expected_user

    user = get_current_user(token="valid_token", user_repository=mock_repo)

    assert user == expected_user
    mock_repo.find_by_id.assert_called_once_with(1)


@patch("config.auth_depends.JWTManager.decode_token")
def test_get_current_user_inactive_or_not_found_raises_unauthorized(mock_decode):
    mock_decode.return_value = {"id": 1}
    mock_repo = MagicMock()
    
    # Simular que el usuario no está activo
    inactive_user = User(id=1, is_active=False)
    mock_repo.find_by_id.return_value = inactive_user

    with pytest.raises(UnauthorizedUser):
        get_current_user(token="valid_token", user_repository=mock_repo)


# --- Pruebas de RoleChecker ---

def test_role_checker_allows_authorized_role():
    user = User(id=1, role=Role.ADMIN)
    checker = RoleChecker(allowed_roles=[Role.ADMIN])

    result = checker(user=user)

    assert result == user


def test_role_checker_raises_forbidden_for_unauthorized_role():
    user = User(id=1, role=Role.USER)
    checker = RoleChecker(allowed_roles=[Role.ADMIN])

    with pytest.raises(ForbiddenException):
        checker(user=user)