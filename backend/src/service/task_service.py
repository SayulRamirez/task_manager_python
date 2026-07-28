from dto.task_dto import CreateTask
from repository.projec_repository import ProjectRepository
from repository.task_repository import TaskRepository
from repository.user_repository import UserRepository


class TaskService:

    def __init__(self, task_repository: TaskRepository, project_repository: ProjectRepository, user_repository: UserRepository):
        self.task_repository = task_repository
        self.project_repository = project_repository
        self.user_repository = user_repository

    def create_task(self, request: CreateTask):
        user = self.user_repository.find_by_email(request.email)
        
        if user \
            and self.project_repository.find_by_id(request.project_id):    
            return self.task_repository.create(request, user.id)
        
        return None

    def get_task(self, id):
        return self.task_repository.find_by_id(id)
    
    def get_tasks_by_responsible(self, id_responsible):
        return self.task_repository.find_all_by_responsible(id_responsible)
    
    def changed_status(self, id, change):
        return self.task_repository.changed_status(id, change)
    
    def deleted(self, id):
        return self.task_repository.deleted(id)
