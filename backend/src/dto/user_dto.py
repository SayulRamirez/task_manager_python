from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class AuthResponse(BaseModel):
    token: str

class UserBase(BaseModel):
    first_name: str = Field(alias='firstName', min_length=1, max_length=20, examples=['Juan'])
    last_name: str = Field(alias='lastName', min_length=1, max_length=20, examples=['Perez'])
    maternal_surname: str = Field(alias='maternalSurname', min_length=1, examples=['Hernadez'])
    phone_number: str = Field(alias='phoneNumber', min_length=10, max_length=15, examples=['37495849265'])

    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        #populate_by_name=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

class UserCredential(BaseModel):
    email: EmailStr = Field(examples=['juan.perez@dominio.com'])
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        #populate_by_name=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

class LoginRequest(UserCredential):
    password: str = Field(min_length=8, max_length=30, examples=['securet'])

class RegisterUser(UserBase, LoginRequest):
    pass

class User(UserBase):
    id: int = Field(gt=0, examples=[4])

class UserResponse(User, UserCredential):
    pass

# class UserResponse(User, UserCredential):
#     status: Literal['ACTIVE', 'BLOCKED', 'DELETED'] = Field()

# class UpdateUser(UserBase):
#     pass

class UpdateUser(BaseModel):
    first_name: Optional[str] = Field(default=None, alias='firstName', min_length=1, max_length=20, examples=['Juan'])
    last_name: Optional[str] = Field(default=None, alias='lastName', min_length=1, max_length=20, examples=['Perez'])
    maternal_surname: Optional[str] = Field(default=None, alias='maternalSurname', min_length=1, max_length=20, examples=['Hernadez'])
    phone_number: Optional[str] = Field(default=None, alias='phoneNumber', min_length=10, max_length=15, examples=['37495849265'])

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