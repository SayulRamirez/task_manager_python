import pytest
from config.hashing import Hasher
from models.user import User


def test_register_success(client):
    payload = {
        "firstName": "Carlos",
        "lastName": "Mendoza",
        "maternalSurname": "Ruiz",
        "phoneNumber": "5551234567",
        "email": "carlos.mendoza@example.com",
        "password": "securePassword123"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "carlos.mendoza@example.com"


def test_register_user_already_exists_returns_409(client, db_session):
    existing_user = User(
        first_name="Carlos",
        last_name="Mendoza",
        maternal_surname="Ruiz",
        phone_number="5551234567",
        email="existing@example.com",
        password=Hasher.hash("securePassword123")
    )
    db_session.add(existing_user)
    db_session.commit()

    payload = {
        "firstName": "Carlos",
        "lastName": "Mendoza",
        "maternalSurname": "Ruiz",
        "phoneNumber": "5551234567",
        "email": "existing@example.com",
        "password": "securePassword123"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "User already exists"


def test_login_success(client, db_session):
    user = User(
        first_name="Login",
        last_name="User",
        maternal_surname="Test",
        phone_number="1234567890",
        email="login_user@example.com",
        password=Hasher.hash("validPassword123"),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

    # OAuth2PasswordRequestForm requiere x-www-form-urlencoded (parámetro data=)
    form_data = {
        "username": "login_user@example.com",
        "password": "validPassword123"
    }

    response = client.post("/auth/login", data=form_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials_returns_401(client):
    form_data = {
        "username": "wrong@example.com",
        "password": "wrongPassword"
    }

    response = client.post("/auth/login", data=form_data)

    assert response.status_code == 401