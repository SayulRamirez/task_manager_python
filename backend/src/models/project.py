from datetime import date
import enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class Status(str, enum.Enum):
    PENDING = 'Pendiente'
    IN_PROGRESS = 'En progreso'
    COMPLETE = 'Completa'

class Project(Base):
    __tablename__ = 'projects'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    owner: Mapped['User'] = relationship(back_populates='projects_owners')
    status: Mapped[Status] = mapped_column(default=Status.PENDING)
    estimated_completion: Mapped[date] = mapped_column(default=date.today)

    tasks_project: Mapped[list['Task']] = relationship(back_populates='project', cascade='all, delete-orphan')