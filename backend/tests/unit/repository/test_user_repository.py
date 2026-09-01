from config.hashing import Hasher
from dto.user_dto import RegisterUser, UpdateUser
from models.user import User
from repository.user_repository import UserRepository


# --- Pruebas de Registro ---

def test_register_user_success(db_session):
    repo = UserRepository(db_session)
    request = RegisterUser(
        firstName="John",
        lastName="Doe",
        maternalSurname='Ma',
        email="john.doe@example.com",
        password="secretpassword123",
        phoneNumber="1234567890"
    )

    user = repo.register(request)

    assert user.id is not None
    assert user.email == "john.doe@example.com"
    assert Hasher.verify("secretpassword123", user.password)


# --- Pruebas de Búsqueda ---

def test_find_by_id(db_session):
    repo = UserRepository(db_session)
    user = User(
        first_name="Jane", 
        last_name="Doe", 
        maternal_surname='Smith',
        phone_number="9476543250", 
        email="jane@example.com", 
        password=Hasher.hash("pass12vs5g43")
    )
    db_session.add(user)
    db_session.commit()

    # Caso exitoso
    found_user = repo.find_by_id(user.id)
    assert found_user is not None
    assert found_user.id == user.id

    # Caso no encontrado
    assert repo.find_by_id(9999) is None


def test_find_by_email(db_session):
    repo = UserRepository(db_session)
    user = User(
        first_name="Alice", 
        last_name="Smith", 
        maternal_surname='Smith',
        phone_number="23876443450", 
        email="alice@example.com", 
        password=Hasher.hash("pass123")
    )
    db_session.add(user)
    db_session.commit()

    # Caso exitoso
    found_user = repo.find_by_email(user.email)
    assert found_user is not None
    assert found_user.email == user.email

    # Caso no encontrado
    assert repo.find_by_email("notfound@example.com") is None


def test_exists_by_phone_number(db_session):
    repo = UserRepository(db_session)
    user = User(
        first_name="Bob", 
        last_name="Marley", 
        maternal_surname='Smith',
        phone_number="9876543210", 
        email="bob@example.com", 
        password=Hasher.hash("pass123")
    )
    db_session.add(user)
    db_session.commit()

    assert repo.exists_by_phone_number("9876543210") is True
    assert repo.exists_by_phone_number("0000000000") is False


# --- Pruebas de Actualización ---

def test_update_user_success(db_session):
    repo = UserRepository(db_session)
    user = User(
        first_name="OriginalName", 
        last_name="User", 
        maternal_surname='Smith',
        phone_number='46264464656',
        email="update@example.com", 
        password=Hasher.hash("pass123")
    )
    db_session.add(user)
    db_session.commit()

    update_dto = UpdateUser(firstName="UpdatedName")
    updated_user = repo.update(user.id, update_dto)

    assert updated_user is not None
    assert updated_user.first_name == "UpdatedName"
    assert updated_user.last_name == "User"  # Mantiene valores no modificados


def test_update_user_not_found(db_session):
    repo = UserRepository(db_session)
    update_dto = UpdateUser(firstName="UpdatedName")

    result = repo.update(9999, update_dto)
    assert result is None


# --- Pruebas de Autenticación ---

def test_authenticate_success(db_session):
    repo = UserRepository(db_session)
    password_raw = "correct_password"
    user = User(
        first_name="Auth", 
        last_name="User", 
        maternal_surname='Smith',
        phone_number='46264287329',
        email="auth@example.com", 
        password=Hasher.hash(password_raw),
    )
    db_session.add(user)
    db_session.commit()
    authenticated_user = repo.authenticate("auth@example.com", password_raw)
    assert authenticated_user is not None
    assert authenticated_user.id == user.id


def test_authenticate_failures(db_session):
    repo = UserRepository(db_session)
    raw_password = "correct_password"
    user = User(
        first_name="Auth", 
        last_name="User", 
        maternal_surname='Smith',
        phone_number='3332984372',
        email="auth_fail@example.com", 
        password=Hasher.hash(raw_password),
    )
    db_session.add(user)
    db_session.commit()

    # 1. Usuario no existe
    assert repo.authenticate("wrong@example.com", raw_password) is None

    # 2. Contraseña incorrecta
    assert repo.authenticate("auth_fail@example.com", "wrong_pass") is None

    # 3. Usuario inactivo (debe fallar con la contraseña correcta en texto plano)
    user.is_active = False
    db_session.commit()
    assert repo.authenticate("auth_fail@example.com", raw_password) is None