from datetime import date
import enum

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base
from models.project import Status

class Priority(str, enum.Enum):
    LOW = 'Baja'
    MEDIUM = 'Media'
    HIGH = 'Alta'

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(20), nullable=False)
    description = Column(String(100), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.PENDING)
    estimated_delivery = Column(Date, nullable=False)
    priority = Column(Enum(Priority), nullable=False)
    create_date = Column(Date, nullable=False, default=date.today)

    id_responsible = Column(Integer, ForeignKey('users.id'))
    responsible = relationship('User', back_populates='tasks_owners')

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', back_populates='tasks_project')