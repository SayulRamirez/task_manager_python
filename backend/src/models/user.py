
import enum

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

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
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    maternal_surname = Column(String(20), nullable=False)
    phone_number = Column(String(15), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    role = Column(Enum(Role), default=Role.USER)

    projects_owners = relationship('Project', back_populates='owner')
    tasks_owners = relationship('Task', back_populates='responsible')