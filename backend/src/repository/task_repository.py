from sqlalchemy.orm import Session

from dto.task_dto import CreateTask
from models.project import Status
from models.task import Task


class TaskRepository():
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, id):
        return self.db.query(Task).filter(Task.id == id).first()
    
    def find_all_by_responsible(self, id_responsible: int):
        return self.db.query(Task).filter(Task.id_responsible == id_responsible).all()

    def create(self, request: CreateTask, responsible: int):
        task = Task(**request.model_dump(exclude={'email'}), id_responsible=responsible)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def changed_status(self, id: int, change: Status):
        task = self.find_by_id(id)
        if task:
            task.status = change
            self.db.commit()
            self.db.refresh(task)
            return task
        return None
    
    def deleted(self, id: int):
        task = self.find_by_id(id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False