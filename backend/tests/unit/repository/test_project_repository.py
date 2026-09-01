from datetime import date, timedelta
import pytest
from dto.project_dto import CreateProject
from models.project import Project, Status
from models.user import User
from repository.projec_repository import ProjectRepository


# --- Fixture auxiliar para asociar la relación de clave foránea ---
@pytest.fixture
def test_user(db_session):
    user = User(
        first_name="Leader",
        last_name="Owner",
        maternal_surname="Project",
        email="leader_project@example.com",
        phone_number="1234567890",
        password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    return user


# --- Pruebas de Creación (save) ---

def test_save_project_success(db_session, test_user):
    repo = ProjectRepository(db_session)
    request = CreateProject(
        title="Sistema CRM",
        description="Módulo de gestión de clientes",
        estimateCompletion=date.today() + timedelta(days=7)
    )

    project = repo.save(user_id=test_user.id, request=request)

    assert project.id is not None
    assert project.title == "Sistema CRM"
    assert project.user_id == test_user.id
    assert project.status == Status.PENDING


# --- Pruebas de Búsqueda (find_by_id) ---

def test_find_by_id_success_and_user_isolation(db_session, test_user):
    project = Project(
        title="Proyecto 1",
        description="Descripción",
        user_id=test_user.id,
        estimated_completion=date.today()
    )
    db_session.add(project)
    db_session.commit()

    repo = ProjectRepository(db_session)

    # 1. Búsqueda exitosa con el usuario correcto
    found_project = repo.find_by_id(id=project.id, user_id=test_user.id)
    assert found_project is not None
    assert found_project.id == project.id

    # 2. Búsqueda fallida si pertenece a otro usuario
    assert repo.find_by_id(id=project.id, user_id=9999) is None

    # 3. Búsqueda con ID inexistente
    assert repo.find_by_id(id=8888, user_id=test_user.id) is None


# --- Pruebas de Listado (get_all) ---

def test_get_all_projects_by_leader(db_session, test_user):
    # Usuario secundario para comprobar aislamiento
    other_user = User(
        first_name="Other",
        last_name="User",
        maternal_surname="Test",
        email="other@example.com",
        phone_number="0987654321",
        password="hashed_password"
    )
    db_session.add(other_user)
    db_session.commit()

    # Proyectos del usuario principal y secundario
    p1 = Project(title="P1", description="D1", user_id=test_user.id)
    p2 = Project(title="P2", description="D2", user_id=test_user.id)
    p3 = Project(title="P3", description="D3", user_id=other_user.id)
    db_session.add_all([p1, p2, p3])
    db_session.commit()

    repo = ProjectRepository(db_session)

    projects = repo.get_all(id_leader=test_user.id)

    assert len(projects) == 2
    assert all(p.user_id == test_user.id for p in projects)


# --- Pruebas de Cambio de Estado (changed_status) ---

def test_changed_status_success(db_session, test_user):
    project = Project(title="P Status", description="Desc", user_id=test_user.id, status=Status.PENDING)
    db_session.add(project)
    db_session.commit()

    repo = ProjectRepository(db_session)

    # Cambiar estado
    updated_project = repo.changed_status(id=project.id, status=Status.IN_PROGRESS, user_id=test_user.id)

    assert updated_project is not None
    assert updated_project.status == Status.IN_PROGRESS


def test_changed_status_unauthorized_user(db_session, test_user):
    project = Project(title="P Status", description="Desc", user_id=test_user.id, status=Status.PENDING)
    db_session.add(project)
    db_session.commit()

    repo = ProjectRepository(db_session)

    # Intentar cambiar estado con un user_id no propietario
    result = repo.changed_status(id=project.id, status=Status.COMPLETE, user_id=9999)

    assert result is None
    # Confirmar que en base de datos no cambió el estado
    db_session.refresh(project)
    assert project.status == Status.PENDING


# --- Pruebas de Eliminación (deleted) ---

def test_deleted_success_and_protection(db_session, test_user):
    project = Project(title="To Delete", description="Desc", user_id=test_user.id)
    db_session.add(project)
    db_session.commit()

    repo = ProjectRepository(db_session)

    # 1. Intentar borrar con usuario incorrecto debe retornar False
    assert repo.deleted(id=project.id, user_id=9999) is False
    assert db_session.query(Project).filter_by(id=project.id).first() is not None

    # 2. Borrar con el propietario correcto debe retornar True
    assert repo.deleted(id=project.id, user_id=test_user.id) is True
    assert db_session.query(Project).filter_by(id=project.id).first() is None