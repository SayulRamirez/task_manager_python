from datetime import date, timedelta
import pytest
from config.hashing import Hasher
from config.jwt import JWTManager
from models.project import Project, Status
from models.user import Role, User


# --- Fixtures de Autenticación y Proyectos ---

@pytest.fixture
def owner_user(db_session):
    user = User(
        first_name="Leader",
        last_name="Owner",
        maternal_surname="Project",
        email="leader_owner@example.com",
        phone_number="1112223334",
        password=Hasher.hash("pass123"),
        role=Role.USER,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def owner_headers(owner_user):
    token = JWTManager.get_token(sub=owner_user.email, user_id=owner_user.id, extra_claims={"role": owner_user.role.value})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_user(db_session):
    user = User(
        first_name="Other",
        last_name="Leader",
        maternal_surname="User",
        email="other_leader@example.com",
        phone_number="9998887776",
        password=Hasher.hash("pass123"),
        role=Role.USER,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def other_headers(other_user):
    token = JWTManager.get_token(sub=other_user.email, user_id=other_user.id, extra_claims={"role": other_user.role.value})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_project(db_session, owner_user):
    project = Project(
        title="Proyecto Base",
        description="Descripción del proyecto base",
        user_id=owner_user.id,
        status=Status.PENDING,
        estimated_completion=date.today() + timedelta(days=10)
    )
    db_session.add(project)
    db_session.commit()
    return project


# --- Pruebas de Creación (POST /project) ---

def test_create_project_success(client, owner_headers):
    payload = {
        "title": "Nuevo Proyecto",
        "description": "Descripción detallada",
        "estimateCompletion": (date.today() + timedelta(days=5)).isoformat()
    }

    response = client.post("/project", json=payload, headers=owner_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Nuevo Proyecto"
    assert data["status"] == Status.PENDING.value
    assert "id" in data


def test_create_project_past_date_validation_error(client, owner_headers):
    payload = {
        "title": "Proyecto Inválido",
        "description": "Fecha en el pasado",
        "estimateCompletion": (date.today() - timedelta(days=1)).isoformat()
    }

    response = client.post("/project", json=payload, headers=owner_headers)

    assert response.status_code == 422


# --- Pruebas de Lectura (GET /project/{id} y GET /project) ---

def test_get_project_by_id_success(client, owner_headers, test_project):
    response = client.get(f"/project/{test_project.id}", headers=owner_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_project.id
    assert data["title"] == test_project.title


def test_get_project_by_id_returns_404_for_other_user(client, other_headers, test_project):
    # Intentar acceder a un proyecto ajeno debe simular un 404 por aislamiento
    response = client.get(f"/project/{test_project.id}", headers=other_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_get_all_by_leader_returns_only_owned_projects(client, db_session, owner_headers, other_user, test_project):
    # Crear un proyecto para el otro usuario
    other_project = Project(
        title="Proyecto Ajeno",
        description="No pertenece al owner",
        user_id=other_user.id
    )
    db_session.add(other_project)
    db_session.commit()

    response = client.get("/project", headers=owner_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == test_project.id


# --- Pruebas de Modificación de Estado (PATCH /project/{id}/changed/{changed}) ---

def test_changed_status_success(client, owner_headers, test_project):
    new_status = Status.IN_PROGRESS.value

    response = client.patch(f"/project/{test_project.id}/changed/{new_status}", headers=owner_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == new_status


def test_changed_status_returns_404_for_unauthorized_user(client, other_headers, test_project):
    new_status = Status.COMPLETE.value

    response = client.patch(f"/project/{test_project.id}/changed/{new_status}", headers=other_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


# --- Pruebas de Eliminación (DELETE /project/{id}) ---

def test_delete_project_returns_404_for_unauthorized_user(client, other_headers, test_project):
    response = client.delete(f"/project/{test_project.id}", headers=other_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_delete_project_success(client, owner_headers, test_project):
    response = client.delete(f"/project/{test_project.id}", headers=owner_headers)

    assert response.status_code == 204
    assert response.text == ""

    # Confirmar que la ruta responda 404 posteriormente
    get_response = client.get(f"/project/{test_project.id}", headers=owner_headers)
    assert get_response.status_code == 404