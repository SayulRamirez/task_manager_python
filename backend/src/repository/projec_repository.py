from sqlalchemy import select

from dto.project_dto import CreateProject
from models.project import Project, Status

from sqlalchemy.orm import Session

class ProjectRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, id: int):
        stmt = select(Project).where(Project.id == id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_all(self, id_leader: int):
        stmt = select(Project).where(Project.user_id == id_leader)
        return self.db.execute(stmt).scalars().all()
    
    def save(self, request: CreateProject) -> Project:
        project = Project(**request.model_dump())
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def changed_status(self, id: int, status: Status):
        project = self.find_by_id(id)

        if project:
            project.status = status
            self.db.commit()
            self.db.refresh(project)
            return project
        return None
    
    def deleted(self, id: int):
        project = self.find_by_id(id)
        if not project:
            return False
        self.db.delete(project)
        self.db.commit()
        return True
