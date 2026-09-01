from config.hashing import Hasher
from dto.user_dto import RegisterUser
from models.user import User
from repository.user_repository import UserRepository
from service.auth_service import AuthService
from unittest.mock import MagicMock, patch


# --- Pruebas de Login ---

def test_login_success(db_session):
    # Arrange: Usuario registrado en la BD de pruebas
    user = User(
        first_name="Auth",
        last_name="User",
        maternal_surname="Test",
        phone_number="1112223334",
        email="login_success@example.com",
        password=Hasher.hash("valid_password123"),
        role="USER",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    repo = UserRepository(db_session)
    service = AuthService(repo)

    # Act
    result = service.login("login_success@example.com", "valid_password123")

    # Assert
    assert result is not None
    assert "access_token" in result
    assert result["token_type"] == "bearer"
    assert isinstance(result["access_token"], str)


def test_login_empty_credentials(db_session):
    repo = UserRepository(db_session)
    service = AuthService(repo)

    # Validar rechazo de valores vacíos antes de ir a la BD
    assert service.login("", "some_password") is None
    assert service.login("user@example.com", "") is None
    assert service.login("", "") is None


def test_login_invalid_credentials(db_session):
    repo = UserRepository(db_session)
    service = AuthService(repo)

    # Usuario no existente
    assert service.login("not_found@example.com", "password123") is None


# --- Pruebas de Registro ---

def test_register_success(db_session):
    repo = UserRepository(db_session)
    service = AuthService(repo)

    request = RegisterUser(
        firstName="New",
        lastName="User",
        maternalSurname="Register",
        email="new_user@example.com",
        password="securepassword123",
        phoneNumber="9988776655"
    )

    user = service.register(request)

    assert user is not None
    assert user.id is not None
    assert user.email == "new_user@example.com"


def test_register_email_already_exists(db_session):
    # Arrange: Crear usuario previo con el mismo email
    existing_user = User(
        first_name="Existing",
        last_name="User",
        maternal_surname="Test",
        phone_number="5544332211",
        email="existing@example.com",
        password=Hasher.hash("pass123")
    )
    db_session.add(existing_user)
    db_session.commit()

    repo = UserRepository(db_session)
    service = AuthService(repo)

    request = RegisterUser(
        firstName="Duplicate",
        lastName="User",
        maternalSurname="Test",
        email="existing@example.com",  # Mismo correo
        password="securepassword123",
        phoneNumber="1231231234"
    )

    # Act & Assert
    result = service.register(request)
    assert result is None





@patch("service.auth_service.JWTManager.get_token")
def test_login_success_with_mocks(mock_get_token):
    # Arrange
    mock_get_token.return_value = "fake_jwt_token"
    mock_repo = MagicMock(spec=UserRepository)
    mock_user = User(id=1, email="carlos@example.com", role="ADMIN")
    mock_repo.authenticate.return_value = mock_user

    service = AuthService(mock_repo)

    # Act
    result = service.login("carlos@example.com", "password123")

    # Assert
    mock_repo.authenticate.assert_called_once_with("carlos@example.com", "password123")
    mock_get_token.assert_called_once_with(
        sub="carlos@example.com",
        user_id=1,
        extra_claims={"role": "ADMIN"}
    )
    assert result == {"access_token": "fake_jwt_token", "token_type": "bearer"}


def test_login_returns_none_when_repo_fails():
    mock_repo = MagicMock(spec=UserRepository)
    mock_repo.authenticate.return_value = None  # Usuario o password incorrectos

    service = AuthService(mock_repo)
    result = service.login("user@example.com", "wrong_pass")

    assert result is None


def test_register_returns_none_if_email_exists():
    mock_repo = MagicMock(spec=UserRepository)
    mock_repo.find_by_email.return_value = User(id=1, email="existing@example.com")

    service = AuthService(mock_repo)
    request = RegisterUser(
        firstName="Test",
        lastName="User",
        maternalSurname="Test",
        email="existing@example.com",
        password="password123",
        phoneNumber="1234567890"
    )

    result = service.register(request)

    # Verifica que al existir el email, ni siquiera intente llamar a repo.register()
    mock_repo.find_by_email.assert_called_once_with("existing@example.com")
    mock_repo.register.assert_not_called()
    assert result is None