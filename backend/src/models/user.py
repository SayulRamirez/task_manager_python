
import enum

from sqlalchemy import Column, Integer, String, Enum

from config.database import Base


class UserStatus(str, enum.Enum):
    ACTIVE = True
    BLOCKED = False
    DELETED = False

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