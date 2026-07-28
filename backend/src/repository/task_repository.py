from datetime import date

from dto.task_dto import CreateTask
from models.task import Task


class TaskRepository():
    tasks: list[Task] = []
    __id_count = 0

    def create(self, request: CreateTask, user_id: int, project_id: int):
        task = Task(self.__id_count, request.title, request.description, user_id, 'PENDING', project_id, request.estimate_delivery, request.priority, date.today())
        self.tasks.append(task)

    def find_by_id(self, id):
        for task in self.tasks:
            if task.id == id:
                return task
        return None
    
    def find_all_by_responsible(self, id_responsible: int):
        return [task for task in self.tasks if task.id_responsible == id_responsible]
    
    def changed_status(self, id: int, change: str):
        task = self.find_by_id(id)
        if not task:
            return None
        task.status = change
        return task
    
    def deleted(self, task):
        task = self.find_by_id(id)
        if not task:
            return False
        self.tasks.remove(task)
        return True
        
