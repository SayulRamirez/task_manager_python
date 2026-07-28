from datetime import date
import enum

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from config.database import Base


class Status(str, enum.Enum):
    PENDING = 'Pendiente'
    IN_PROGRESS = 'En progreso'
    COMPLETE = 'Completa'

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(20), nullable=False)
    description = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='projects_owners')
    status = Column(Enum(Status), default=Status.PENDING)
    estimated_completion = Column(Date, nullable=False, default=date.today)

    tasks_project = relationship('Task', back_populates='project', cascade='all, delete-orphan')