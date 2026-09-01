from datetime import date, timedelta
import pytest
from config.hashing import Hasher
from config.jwt import JWTManager
from models.project import Project, Status
from models.task import Task
from models.user import Role, User


# --- Fixtures de Autenticación, Proyectos y Tareas ---

@pytest.fixture
def owner_user(db_session):
    user = User(
        first_name="Project",
        last_name="Owner",
        maternal_surname="User",
        email="owner_task@example.com",
        phone_number="1111111111",
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
def responsible_user(db_session):
    user = User(
        first_name="Task",
        last_name="Responsible",
        maternal_surname="User",
        email="responsible_task@example.com",
        phone_number="2222222222",
        password=Hasher.hash("pass123"),
        role=Role.USER,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def responsible_headers(responsible_user):
    token = JWTManager.get_token(sub=responsible_user.email, user_id=responsible_user.id, extra_claims={"role": responsible_user.role.value})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_user(db_session):
    user = User(
        first_name="Other",
        last_name="User",
        maternal_surname="Test",
        email="other_task_user@example.com",
        phone_number="3333333333",
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
        title="Proyecto Tareas",
        description="Contenedor de tareas de prueba",
        user_id=owner_user.id
    )
    db_session.add(project)
    db_session.commit()
    return project


@pytest.fixture
def test_task(db_session, responsible_user, test_project):
    task = Task(
        title="Tarea Existente",
        description="Descripción tarea test",
        estimated_delivery=date.today() + timedelta(days=5),
        priority="Media",
        status=Status.PENDING,
        project_id=test_project.id,
        id_responsible=responsible_user.id
    )
    db_session.add(task)
    db_session.commit()
    return task


# --- Pruebas de Creación (POST /task) ---

def test_create_task_success(client, owner_headers, responsible_user, test_project):
    payload = {
        "title": "Nueva Tarea",
        "description": "Detalle de la tarea",
        "estimateDelivery": (date.today() + timedelta(days=3)).isoformat(),
        "priority": "Alta",
        "email": responsible_user.email,
        "projectId": test_project.id
    }

    response = client.post("/task", json=payload, headers=owner_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Nueva Tarea"


def test_create_task_returns_404_when_user_or_project_invalid(client, owner_headers, test_project):
    payload = {
        "title": "Tarea Invalida",
        "description": "Prueba error 404 por correo no existente",
        "estimateDelivery": (date.today() + timedelta(days=3)).isoformat(),
        "priority": "Baja",
        "email": "not_found@example.com",
        "projectId": test_project.id
    }

    response = client.post("/task", json=payload, headers=owner_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Project or user not found"


# --- Pruebas de Lectura (GET /task/{id} y GET /task/{id_responsible}/responsible) ---

def test_get_task_by_id_success(client, responsible_headers, test_task):
    response = client.get(f"/task/{test_task.id}", headers=responsible_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_task.id
    assert data["title"] == test_task.title


def test_get_task_by_id_not_found(client, responsible_headers):
    response = client.get("/task/99999", headers=responsible_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_get_tasks_by_responsible_success(client, responsible_headers, responsible_user, test_task):
    response = client.get(f"/task/{responsible_user.id}/responsible", headers=responsible_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["id"] == test_task.id


def test_get_tasks_by_responsible_empty_returns_404(client, owner_headers, owner_user):
    # El usuario owner_user no tiene tareas asignadas como responsable
    response = client.get(f"/task/{owner_user.id}/responsible", headers=owner_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Not foudn tasks wiht user"


# --- Pruebas de Cambio de Estado (PATCH /task/{id}/change/{change}) ---

def test_changed_status_by_responsible_user_success(client, responsible_headers, test_task):
    new_status = Status.IN_PROGRESS.value

    response = client.patch(f"/task/{test_task.id}/change/{new_status}", headers=responsible_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == new_status


def test_changed_status_by_non_responsible_user_returns_404(client, other_headers, test_task):
    new_status = Status.COMPLETE.value

    response = client.patch(f"/task/{test_task.id}/change/{new_status}", headers=other_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# --- Pruebas de Eliminación (DELETE /task/{id}) ---

def test_delete_task_by_non_responsible_user_returns_404(client, other_headers, test_task):
    response = client.delete(f"/task/{test_task.id}", headers=other_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task_by_responsible_user_success(client, responsible_headers, test_task):
    response = client.delete(f"/task/{test_task.id}", headers=responsible_headers)

    assert response.status_code == 204
    assert response.text == ""

    # Validar que ya no exista
    get_response = client.get(f"/task/{test_task.id}", headers=responsible_headers)
    assert get_response.status_code == 404