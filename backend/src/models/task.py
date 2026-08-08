from datetime import date
import enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from config.database import Base
from models.project import Status

class Priority(str, enum.Enum):
    LOW = 'Baja'
    MEDIUM = 'Media'
    HIGH = 'Alta'

class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(100))
    status: Mapped[Status] = mapped_column(default=Status.PENDING)
    estimated_delivery: Mapped[date]
    priority: Mapped[Priority] = mapped_column(default=Priority.MEDIUM)
    create_date: Mapped[date] = mapped_column(default=date.today)

    id_responsible: Mapped[int] = mapped_column(ForeignKey('users.id'))
    responsible: Mapped['User'] = relationship(back_populates='tasks_owners')

    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))
    project: Mapped["Project"] = relationship(back_populates='tasks_project')