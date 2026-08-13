from dto.project_dto import CreateProject
from models.project import Status
from repository.projec_repository import ProjectRepository
from repository.user_repository import UserRepository


class ProjectService:

    def __init__(self, project_repository: ProjectRepository, user_repository: UserRepository):
        self.project_repository = project_repository
        self.user_repository = user_repository

    def create_project(self, user_id: int, request: CreateProject):
        return self.project_repository.save(user_id, request)
    
    def get_project_by_id(self, id: int, user_id: int):
        return self.project_repository.find_by_id(id, user_id)
    
    def get_all_by_leader(self, id_leader: int):
        return self.project_repository.get_all(id_leader)
    
    def changed_status(self, id, status: Status, user_id: int):
        return self.project_repository.changed_status(id, status, user_id)
    
    def deleted(self, id, user_id: int):
        return self.project_repository.deleted(id, user_id)
    
    
