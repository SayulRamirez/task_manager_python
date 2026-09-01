from datetime import date, timedelta
from unittest.mock import MagicMock
import pytest

from dto.task_dto import CreateTask
from models.project import Project, Status
from models.task import Priority, Task
from models.user import User
from repository.projec_repository import ProjectRepository
from repository.task_repository import TaskRepository
from repository.user_repository import UserRepository
from service.task_service import TaskService


# ==============================================================================
# 1. PRUEBAS UNITARIAS PURAS (USANDO MOCKS)
# ==============================================================================

@pytest.fixture
def mock_task_repo():
    return MagicMock(spec=TaskRepository)


@pytest.fixture
def mock_project_repo():
    return MagicMock(spec=ProjectRepository)


@pytest.fixture
def mock_user_repo():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def service_mocked(mock_task_repo, mock_project_repo, mock_user_repo):
    return TaskService(
        task_repository=mock_task_repo,
        project_repository=mock_project_repo,
        user_repository=mock_user_repo
    )


def test_mock_create_task_success(service_mocked, mock_user_repo, mock_project_repo, mock_task_repo):
    request = MagicMock(spec=CreateTask)
    request.email = "assigned@example.com"
    request.project_id = 10

    assigned_user = MagicMock(spec=User)
    assigned_user.id = 55
    mock_user_repo.find_by_email.return_value = assigned_user

    project = MagicMock(spec=Project)
    mock_project_repo.find_by_id.return_value = project

    expected_task = Task(id=1, title="Tarea Mock", id_responsible=55)
    mock_task_repo.create.return_value = expected_task

    # El creador del proyecto es user_id = 1
    result = service_mocked.create_task(request=request, user_id=1)

    mock_user_repo.find_by_email.assert_called_once_with("assigned@example.com")
    mock_project_repo.find_by_id.assert_called_once_with(10, 1)
    mock_task_repo.create.assert_called_once_with(request, 55)
    assert result == expected_task


def test_mock_create_task_fails_when_user_not_found(service_mocked, mock_user_repo, mock_task_repo):
    request = MagicMock(spec=CreateTask)
    request.email = "nonexistent@example.com"

    mock_user_repo.find_by_email.return_value = None

    result = service_mocked.create_task(request=request, user_id=1)

    assert result is None
    mock_task_repo.create.assert_not_called()


def test_mock_create_task_fails_when_project_not_found(service_mocked, mock_user_repo, mock_project_repo, mock_task_repo):
    request = MagicMock(spec=CreateTask)
    request.email = "assigned@example.com"
    request.project_id = 99

    mock_user_repo.find_by_email.return_value = MagicMock(spec=User)
    mock_project_repo.find_by_id.return_value = None  # El proyecto no existe o no es del líder

    result = service_mocked.create_task(request=request, user_id=1)

    assert result is None
    mock_task_repo.create.assert_not_called()


def test_mock_get_task_delegates(service_mocked, mock_task_repo):
    expected_task = Task(id=1)
    mock_task_repo.find_by_id.return_value = expected_task

    result = service_mocked.get_task(id=1)

    mock_task_repo.find_by_id.assert_called_once_with(1)
    assert result == expected_task


def test_mock_get_tasks_by_responsible_delegates(service_mocked, mock_task_repo):
    mock_task_repo.find_all_by_responsible.return_value = [Task(id=1), Task(id=2)]

    result = service_mocked.get_tasks_by_responsible(id_responsible=55)

    mock_task_repo.find_all_by_responsible.assert_called_once_with(55)
    assert len(result) == 2


def test_mock_changed_status_delegates(service_mocked, mock_task_repo):
    updated = Task(id=1, status=Status.COMPLETE)
    mock_task_repo.changed_status.return_value = updated

    result = service_mocked.changed_status(id=1, change=Status.COMPLETE, user_id=55)

    mock_task_repo.changed_status.assert_called_once_with(1, Status.COMPLETE, 55)
    assert result == updated


def test_mock_deleted_delegates(service_mocked, mock_task_repo):
    mock_task_repo.deleted.return_value = True

    result = service_mocked.deleted(id=1, user_id=55)

    mock_task_repo.deleted.assert_called_once_with(1, 55)
    assert result is True


# ==============================================================================
# 2. PRUEBAS CON BASE DE DATOS EN MEMORIA (USANDO db_session)
# ==============================================================================

@pytest.fixture
def service_db(db_session):
    return TaskService(
        task_repository=TaskRepository(db_session),
        project_repository=ProjectRepository(db_session),
        user_repository=UserRepository(db_session)
    )


@pytest.fixture
def owner_user(db_session):
    user = User(
        first_name="Project",
        last_name="Owner",
        maternal_surname="User",
        email="owner@example.com",
        phone_number="1111111111",
        password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def responsible_user(db_session):
    user = User(
        first_name="Task",
        last_name="Responsible",
        maternal_surname="User",
        email="responsible@example.com",
        phone_number="2222222222",
        password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def test_project(db_session, owner_user):
    project = Project(
        title="Proyecto de Integración",
        description="Descripción del proyecto",
        user_id=owner_user.id
    )
    db_session.add(project)
    db_session.commit()
    return project


def test_db_create_task_success(service_db, owner_user, responsible_user, test_project):
    request = CreateTask(
        title="Crear Documentación",
        description="Escribir OpenAPI spec",
        estimateDelivery=date.today() + timedelta(days=2),
        priority=Priority.MEDIUM,
        email=responsible_user.email,
        project_id=test_project.id
    )

    task = service_db.create_task(request=request, user_id=owner_user.id)

    assert task is not None
    assert task.id is not None
    assert task.id_responsible == responsible_user.id
    assert task.project_id == test_project.id


def test_db_create_task_fails_if_email_not_found(service_db, owner_user, test_project):
    request = CreateTask(
        title="Tarea Invalida",
        description="Sin usuario existente",
        estimateDelivery=date.today() + timedelta(days=2),
        priority=Priority.LOW,
        email="nonexistent@domain.com",
        project_id=test_project.id
    )

    result = service_db.create_task(request=request, user_id=owner_user.id)
    assert result is None


def test_db_create_task_fails_if_project_not_owned_by_user(service_db, responsible_user, test_project):
    # El usuario responsable intenta crear una tarea en un proyecto que pertenece al creador (owner)
    request = CreateTask(
        title="Tarea No Autorizada",
        description="Test de proyecto ajeno",
        estimateDelivery=date.today() + timedelta(days=2),
        priority=Priority.MEDIUM,
        email=responsible_user.email,
        project_id=test_project.id
    )

    result = service_db.create_task(request=request, user_id=responsible_user.id)
    assert result is None


def test_db_get_task_and_get_tasks_by_responsible(service_db, db_session, responsible_user, test_project):
    task = Task(
        title="Tarea DB",
        description="Desc",
        project_id=test_project.id,
        id_responsible=responsible_user.id,
        estimated_delivery=date.today() + timedelta(days=2)
    )
    db_session.add(task)
    db_session.commit()

    # Búsqueda individual
    found = service_db.get_task(id=task.id)
    assert found is not None
    assert found.id == task.id

    # Búsqueda por responsable
    responsible_tasks = service_db.get_tasks_by_responsible(id_responsible=responsible_user.id)
    assert len(responsible_tasks) == 1
    assert responsible_tasks[0].id == task.id


def test_db_changed_status_and_deleted(service_db, db_session, responsible_user, test_project):
    task = Task(
        title="Tarea Operaciones",
        description="Desc",
        project_id=test_project.id,
        id_responsible=responsible_user.id,
        status=Status.PENDING,
        estimated_delivery=date.today() + timedelta(days=2)
    )
    db_session.add(task)
    db_session.commit()

    # Actualizar Estado
    updated = service_db.changed_status(id=task.id, change=Status.IN_PROGRESS, user_id=responsible_user.id)
    assert updated is not None
    assert updated.status == Status.IN_PROGRESS

    # Eliminar Tarea
    assert service_db.deleted(id=task.id, user_id=responsible_user.id) is True
    assert service_db.get_task(id=task.id) is None