from datetime import date, timedelta
import pytest

from dto.task_dto import CreateTask
from models.project import Project, Status
from models.task import Priority, Task
from models.user import User
from repository.task_repository import TaskRepository


# --- Fixtures de apoyo para la integridad referencial (FKs) ---

@pytest.fixture
def test_user(db_session):
    user = User(
        first_name="Task",
        last_name="Responsible",
        maternal_surname="User",
        email="task_responsible@example.com",
        phone_number="1234567890",
        password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def test_project(db_session, test_user):
    project = Project(
        title="Proyecto Contenedor",
        description="Proyecto asignado para las tareas",
        user_id=test_user.id
    )
    db_session.add(project)
    db_session.commit()
    return project


# --- Pruebas de Creación (create) ---

def test_create_task_success(db_session, test_user, test_project):
    repo = TaskRepository(db_session)
    request = CreateTask(
        title="Diseñar Mockups",
        description="Crear los esquemas de pantalla",
        estimateDelivery=date.today() + timedelta(days=3),
        priority=Priority.MEDIUM,
        email="notificacion@dominio.com",  # Debe ignorarse según el repositorio
        project_id=test_project.id
    )

    task = repo.create(request=request, responsible=test_user.id)

    assert task.id is not None
    assert task.title == "Diseñar Mockups"
    assert task.id_responsible == test_user.id
    assert task.project_id == test_project.id


# --- Pruebas de Búsqueda (find_by_id & find_all_by_responsible) ---

def test_find_by_id(db_session, test_user, test_project):
    task = Task(
        title="Tarea Búsqueda",
        description="Descripción",
        estimated_delivery=date.today(),
        priority="Alta",
        project_id=test_project.id,
        id_responsible=test_user.id
    )
    db_session.add(task)
    db_session.commit()

    repo = TaskRepository(db_session)

    # Caso exitoso
    found = repo.find_by_id(task.id)
    assert found is not None
    assert found.id == task.id

    # Caso inexistente
    assert repo.find_by_id(9999) is None


def test_find_all_by_responsible_filters_correctly(db_session, test_user, test_project):
    other_user = User(
        first_name="Otro",
        last_name="Usuario",
        maternal_surname="Test",
        email="other_resp@example.com",
        phone_number="0987654321",
        password="hashed_password"
    )
    db_session.add(other_user)
    db_session.commit()

    delivery = date.today() + timedelta(days=2)

    t1 = Task(title="T1", description="D1", project_id=test_project.id, id_responsible=test_user.id, estimated_delivery=delivery)
    t2 = Task(title="T2", description="D2", project_id=test_project.id, id_responsible=test_user.id, estimated_delivery=delivery)
    t3 = Task(title="T3", description="D3", project_id=test_project.id, id_responsible=other_user.id, estimated_delivery=delivery)
    db_session.add_all([t1, t2, t3])
    db_session.commit()

    repo = TaskRepository(db_session)
    tasks = repo.find_all_by_responsible(test_user.id)

    assert len(tasks) == 2
    assert all(t.id_responsible == test_user.id for t in tasks)


# --- Pruebas de Cambio de Estado (changed_status) ---

def test_changed_status_success_and_protection(db_session, test_user, test_project):
    task = Task(
        title="Tarea Estado",
        description="Descripción",
        project_id=test_project.id,
        id_responsible=test_user.id,
        status=Status.PENDING,
        estimated_delivery=date.today() + timedelta(days=2)
    )
    db_session.add(task)
    db_session.commit()

    repo = TaskRepository(db_session)

    # 1. Fallo: Un usuario no asignado intenta cambiar el estado
    assert repo.changed_status(id=task.id, change=Status.IN_PROGRESS, user_id=9999) is None

    # 2. Éxito: El usuario responsable cambia el estado
    updated_task = repo.changed_status(id=task.id, change=Status.IN_PROGRESS, user_id=test_user.id)
    assert updated_task is not None
    assert updated_task.status == Status.IN_PROGRESS


# --- Pruebas de Eliminación (deleted) ---

def test_deleted_success_and_protection(db_session, test_user, test_project):
    task = Task(
        title="Tarea Borrado",
        description="Descripción",
        project_id=test_project.id,
        id_responsible=test_user.id,
        estimated_delivery=date.today() + timedelta(days=2)
    )
    db_session.add(task)
    db_session.commit()

    repo = TaskRepository(db_session)

    # 1. Fallo: Un usuario no asignado intenta borrar
    assert repo.deleted(id=task.id, user_id=9999) is False
    assert db_session.query(Task).filter_by(id=task.id).first() is not None

    # 2. Éxito: El usuario responsable borra la tarea
    assert repo.deleted(id=task.id, user_id=test_user.id) is True
    assert db_session.query(Task).filter_by(id=task.id).first() is None