from re import Pattern
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class AuthResponse(BaseModel):
    token: str

class UserBase(BaseModel):
    first_name: str = Field(alias='firstName', min_length=1, max_length=20)
    last_name: str = Field(alias='lastName', min_length=1, max_length=20)
    maternal_surname: str = Field(alias='maternalSurname', min_length=1, max_length=20)
    phone_number: str = Field(alias='phoneNumber', min_length=10, max_length=15)

    model_config = ConfigDict(populate_by_name=True)

class UserCredential(BaseModel):
    email: EmailStr

class LoginRequest(UserCredential):
    password: str = Field(min_length=8, max_length=30)

class RegisterUser(UserBase, LoginRequest):
    pass

class User(UserBase):
    id: int = Field(gt=0)

class UserResponse(User, UserCredential):
    status: Literal['ACTIVE', 'BLOCKED', 'DELETED'] = Field()

# class UpdateUser(UserBase):
#     pass

class UpdateUser(BaseModel):
    first_name: Optional[str] = Field(default=None, alias='firstName', min_length=1, max_length=20)
    last_name: Optional[str] = Field(default=None, alias='lastName', min_length=1, max_length=20)
    maternal_surname: Optional[str] = Field(default=None, alias='maternalSurname', min_length=1, max_length=20)
    phone_number: Optional[str] = Field(default=None, alias='phoneNumber', min_length=10, max_length=15)



class StatusUserRequest(BaseModel):
    id: int = Field(gt=0)
    status: Literal['ACTIVE', 'BLOCKED', 'DELETED'] = Field()


class TaskRequest(BaseModel):
    title: str = Field(min_length=3, max_length=25)
    description: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=5, pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$")
    project: int = Field(gt=0)
    estimate_delivery: str = Field(alias='estimateDelivery')
    priority: Literal['LOW', 'MEDIUM', 'HIGH'] = Field()
    
class TaskResponse(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=3, max_length=25)
    description: str = Field(min_length=3, max_length=100)
    status: Literal['COMPLETE', 'IN_PROGRESS', 'PENDING'] = Field()
    estimate_delivery: str = Field(alias='estimateDelivery')
    priority: Literal['LOW', 'MEDIUM', 'HIGH'] = Field()
    create_date: str = Field(alias='createDate')
    runtime: int = Field(gt=0)



class ProjectRequest(BaseModel):
    title: str = Field(min_length=3, max_length=25)
    description: str = Field(min_length=3, max_length=100)
    leader: str = Field(gt=0)
    estimate_completion: str = Field()

class ProjectResponse(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    status: Literal['COMPLETE', 'IN_PROGRESS', 'PENDING'] = Field()
    estimated_completion: str = Field(alias='estimatedCompletion')

class ChangedStatus(BaseModel):
    id: int = Field(gt=0)
    status: Literal['COMPLETE', 'IN_PROGRESS', 'PENDING'] = Field()