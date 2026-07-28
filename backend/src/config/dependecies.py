from fastapi import Depends

from sqlalchemy.orm import Session

from config.database import get_db
from repository.projec_repository import ProjectRepository
from repository.user_repository import UserRepository
from service.auth_service import AuthService
from service.project_service import ProjectService
from service.user_service import UserService


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository)

def get_auth_service(repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repository)


def get_project_repository(db: Session = Depends(get_db)) -> ProjectRepository:
    return ProjectRepository(db)

def get_project_service(project_repository: ProjectRepository = Depends(get_project_repository),
                        user_repository: UserRepository = Depends(get_user_repository)) -> ProjectService:
    return ProjectService(project_repository, user_repository)