from dto.project_dto import CreateProject
from models.project import Project
from repository.projec_repository import ProjectRepository
from repository.user_repository import UserRepository


class ProjectService:

    def __init__(self):
        self.project_repository = ProjectRepository()
        self.user_repository = UserRepository()

    def create_project(self, request: CreateProject):
        if not self.user_repository.find_by_id(request.leader):
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
    
    
