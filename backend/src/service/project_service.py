from dto.project_dto import CreateProject
from repository.projec_repository import ProjectRepository
from repository.user_repository import UserRepository


class ProjectService:

    def __init__(self, project_repository: ProjectRepository, user_repository: UserRepository):
        self.project_repository = project_repository
        self.user_repository = user_repository

    def create_project(self, request: CreateProject):
        if not self.user_repository.find_by_id(request.user_id):
            return None
        return self.project_repository.save(request)
    
    def get_project_by_id(self, id: int):
        return self.project_repository.find_by_id(id)
    
    def get_all_by_leader(self, id_leader: int):
        return self.project_repository.get_all(id_leader)
    
    def changed_status(self, id, status: str):
        return self.project_repository.changed_status(id, status)
    
    def deleted(self, id):
        return self.project_repository.deleted(id)
    
    
