
import enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class UserStatus(str, enum.Enum):
    ACTIVE = 'ACTIVE'
    BLOCKED = 'BLOCKED'
    DELETED = 'DELETED'

class Role(str, enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    maternal_surname: Mapped[str | None] = mapped_column(String(20))
    phone_number: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    status: Mapped[UserStatus] = mapped_column(default=UserStatus.ACTIVE)
    role: Mapped[Role] = mapped_column(default=Role.USER)

    projects_owners: Mapped[list['Project']] = relationship(back_populates='owner')
    tasks_owners: Mapped[list['Task']] = relationship(back_populates='responsible')