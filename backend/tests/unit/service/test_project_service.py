from datetime import date, timedelta
from unittest.mock import MagicMock
import pytest

from dto.project_dto import CreateProject
from models.project import Project, Status
from models.user import User
from repository.projec_repository import ProjectRepository
from repository.user_repository import UserRepository
from service.project_service import ProjectService


# ==============================================================================
# 1. PRUEBAS UNITARIAS PURAS (USANDO MOCKS - AISLAMIENTO TOTAL)
# ==============================================================================

@pytest.fixture
def mock_project_repo():
    return MagicMock(spec=ProjectRepository)


@pytest.fixture
def mock_user_repo():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def service_mocked(mock_project_repo, mock_user_repo):
    return ProjectService(project_repository=mock_project_repo, user_repository=mock_user_repo)


def test_mock_create_project_delegates_to_repo(service_mocked, mock_project_repo):
    request = MagicMock(spec=CreateProject)
    expected_project = Project(id=1, title="Proyecto Mock")
    mock_project_repo.save.return_value = expected_project

    result = service_mocked.create_project(user_id=1, request=request)

    mock_project_repo.save.assert_called_once_with(1, request)
    assert result == expected_project


def test_mock_get_project_by_id_delegates_to_repo(service_mocked, mock_project_repo):
    expected_project = Project(id=5, title="Proyecto Búsqueda")
    mock_project_repo.find_by_id.return_value = expected_project

    result = service_mocked.get_project_by_id(id=5, user_id=1)

    mock_project_repo.find_by_id.assert_called_once_with(5, 1)
    assert result == expected_project


def test_mock_get_all_by_leader_delegates_to_repo(service_mocked, mock_project_repo):
    mock_project_repo.get_all.return_value = [Project(id=1), Project(id=2)]

    result = service_mocked.get_all_by_leader(id_leader=10)

    mock_project_repo.get_all.assert_called_once_with(10)
    assert len(result) == 2


def test_mock_changed_status_delegates_to_repo(service_mocked, mock_project_repo):
    updated_project = Project(id=1, status=Status.IN_PROGRESS)
    mock_project_repo.changed_status.return_value = updated_project

    result = service_mocked.changed_status(id=1, status=Status.IN_PROGRESS, user_id=2)

    mock_project_repo.changed_status.assert_called_once_with(1, Status.IN_PROGRESS, 2)
    assert result == updated_project


def test_mock_deleted_delegates_to_repo(service_mocked, mock_project_repo):
    mock_project_repo.deleted.return_value = True

    result = service_mocked.deleted(id=1, user_id=2)

    mock_project_repo.deleted.assert_called_once_with(1, 2)
    assert result is True


# ==============================================================================
# 2. PRUEBAS CON BASE DE DATOS EN MEMORIA (USANDO db_session)
# ==============================================================================

@pytest.fixture
def service_db(db_session):
    project_repo = ProjectRepository(db_session)
    user_repo = UserRepository(db_session)
    return ProjectService(project_repository=project_repo, user_repository=user_repo)


@pytest.fixture
def test_user(db_session):
    user = User(
        first_name="Service",
        last_name="Leader",
        maternal_surname="Test",
        email="service_leader@example.com",
        phone_number="1234567890",
        password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_db_create_project_success(service_db, test_user):
    request = CreateProject(
        title="Proyecto DB",
        description="Descripción real en SQLite",
        estimateCompletion=date.today() + timedelta(days=5)
    )

    project = service_db.create_project(user_id=test_user.id, request=request)

    assert project is not None
    assert project.id is not None
    assert project.title == "Proyecto DB"
    assert project.user_id == test_user.id


def test_db_get_project_by_id(service_db, test_user, db_session):
    project = Project(title="Proyecto Búsqueda", description="Test", user_id=test_user.id)
    db_session.add(project)
    db_session.commit()

    found = service_db.get_project_by_id(id=project.id, user_id=test_user.id)
    assert found is not None
    assert found.id == project.id
    assert service_db.get_project_by_id(id=project.id, user_id=9999) is None


def test_db_get_all_by_leader(service_db, test_user, db_session):
    p1 = Project(title="P1", description="D1", user_id=test_user.id)
    p2 = Project(title="P2", description="D2", user_id=test_user.id)
    db_session.add_all([p1, p2])
    db_session.commit()

    projects = service_db.get_all_by_leader(id_leader=test_user.id)

    assert len(projects) == 2
    assert all(p.user_id == test_user.id for p in projects)


def test_db_changed_status(service_db, test_user, db_session):
    project = Project(title="P Status", description="Test", user_id=test_user.id, status=Status.PENDING)
    db_session.add(project)
    db_session.commit()

    updated = service_db.changed_status(id=project.id, status=Status.IN_PROGRESS, user_id=test_user.id)

    assert updated is not None
    assert updated.status == Status.IN_PROGRESS


def test_db_deleted(service_db, test_user, db_session):
    project = Project(title="P Delete", description="Test", user_id=test_user.id)
    db_session.add(project)
    db_session.commit()

    assert service_db.deleted(id=project.id, user_id=9999) is False
    assert service_db.deleted(id=project.id, user_id=test_user.id) is True