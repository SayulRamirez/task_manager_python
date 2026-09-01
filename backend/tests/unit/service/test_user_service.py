from unittest.mock import MagicMock
from config.hashing import Hasher
from dto.user_dto import UpdateUser
from models.user import User
from repository.user_repository import UserRepository
from service.user_service import UserService


# --- Pruebas de Integración Ligera (Uso de db_session en memoria) ---

def test_get_info_success(db_session):
    user = User(
        first_name="Carlos",
        last_name="Gomez",
        maternal_surname="Lopez",
        email="carlos@example.com",
        phone_number="1234567890",
        password=Hasher.hash("pass123")
    )
    db_session.add(user)
    db_session.commit()

    repo = UserRepository(db_session)
    service = UserService(repo)

    result = service.get_info(user.id)

    assert result is not None
    assert result.id == user.id
    assert result.email == "carlos@example.com"


def test_get_info_not_found(db_session):
    repo = UserRepository(db_session)
    service = UserService(repo)

    result = service.get_info(9999)

    assert result is None


def test_update_info_success(db_session):
    user = User(
        first_name="Original",
        last_name="User",
        maternal_surname="Test",
        email="service_update@example.com",
        phone_number="0987654321",
        password=Hasher.hash("pass123")
    )
    db_session.add(user)
    db_session.commit()

    repo = UserRepository(db_session)
    service = UserService(repo)

    update_dto = UpdateUser(firstName="UpdatedService")
    updated_user = service.update_info(user.id, update_dto)

    assert updated_user is not None
    assert updated_user.first_name == "UpdatedService"
    assert updated_user.last_name == "User"


def test_update_info_not_found(db_session):
    repo = UserRepository(db_session)
    service = UserService(repo)

    update_dto = UpdateUser(firstName="UpdatedService")
    result = service.update_info(9999, update_dto)

    assert result is None


# --- Pruebas Unitarias Puras (Uso de Mocks sin BD) ---

def test_get_info_delegates_to_repository():
    mock_repo = MagicMock(spec=UserRepository)
    expected_user = User(id=1, first_name="MockedUser")
    mock_repo.find_by_id.return_value = expected_user

    service = UserService(mock_repo)
    result = service.get_info(1)

    mock_repo.find_by_id.assert_called_once_with(1)
    assert result == expected_user


def test_update_info_delegates_to_repository():
    mock_repo = MagicMock(spec=UserRepository)
    update_dto = UpdateUser(firstName="MockName")
    mock_repo.update.return_value = User(id=1, first_name="MockName")

    service = UserService(mock_repo)
    result = service.update_info(1, update_dto)

    mock_repo.update.assert_called_once_with(1, update_dto)

    assert result != None
    assert result.first_name == "MockName"