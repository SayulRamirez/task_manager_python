import pytest
from config.hashing import Hasher
from config.jwt import JWTManager
from models.user import Role, User


# --- Fixtures de Autenticación y Encabezados ---

@pytest.fixture
def admin_user(db_session):
    admin = User(
        first_name="Admin",
        last_name="System",
        maternal_surname="Root",
        phone_number="0000000000",
        email="admin@example.com",
        password=Hasher.hash("adminPass123"),
        role=Role.ADMIN,
        is_active=True
    )
    db_session.add(admin)
    db_session.commit()
    return admin


@pytest.fixture
def admin_headers(admin_user):
    token = JWTManager.get_token(sub=admin_user.email, user_id=admin_user.id, extra_claims={"role": admin_user.role.value})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def regular_user(db_session):
    user = User(
        first_name="Regular",
        last_name="User",
        maternal_surname="Test",
        phone_number="1111111111",
        email="user@example.com",
        password=Hasher.hash("userPass123"),
        role=Role.USER,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def regular_headers(regular_user):
    token = JWTManager.get_token(sub=regular_user.email, user_id=regular_user.id, extra_claims={"role": regular_user.role.value})
    return {"Authorization": f"Bearer {token}"}


# --- Pruebas de Endpoints ---

def test_get_user_info_as_admin_success(client, admin_headers, regular_user):
    response = client.get(f"/user/{regular_user.id}", headers=admin_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == regular_user.email


def test_get_user_info_not_found(client, admin_headers):
    response = client.get("/user/99999", headers=admin_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "User with 99999 not found"


def test_get_user_info_forbidden_for_regular_user(client, regular_headers, regular_user):
    # Intentar acceder con rol USER cuando se exige required_admin
    response = client.get(f"/user/{regular_user.id}", headers=regular_headers)

    assert response.status_code == 403


def test_get_user_info_unauthorized_without_token(client, regular_user):
    response = client.get(f"/user/{regular_user.id}")

    assert response.status_code == 401


def test_update_user_as_admin_success(client, admin_headers, regular_user):
    payload = {
        "firstName": "UpdatedName",
        "lastName": "UpdatedLastName"
    }

    response = client.patch(f"/user/{regular_user.id}", json=payload, headers=admin_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["firstName"] == "UpdatedName"


def test_update_user_not_found(client, admin_headers):
    payload = {"firstName": "UpdatedName"}

    response = client.patch("/user/99999", json=payload, headers=admin_headers)

    assert response.status_code == 404