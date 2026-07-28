from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class TaskBase(BaseModel):
    title: str = Field(min_length=3, max_length=25, examples=['Tarea 1'])
    description: str = Field(min_length=3, max_length=100, examples=['Descripción de la tarea 1'])
    estimate_delivery: date = Field(alias='estimateDelivery', examples=['2026-08-15'])
    priority: Literal['LOW', 'MEDIUM', 'HIGH'] = Field(examples=['MEDIUM'])
    model_config=ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        from_attributes=True,
        validate_by_alias=True,
        validate_by_name=True
    )


class CreateTask(TaskBase):
    email: EmailStr = Field(examples=['juan.perez@dominio.com'])
    project: int = Field(gt=0, examples=[6])
    
    @field_validator('estimate_delivery')
    @classmethod
    def validate_feature_date(cls, value: date):
        if value < date.today():
            raise ValueError('La fecha estimada no puede estar en el pasado')
        return value

class TaskResponse(BaseModel):
    id: int = Field(gt=0, examples=[15])
    status: Literal['COMPLETE', 'IN_PROGRESS', 'PENDING'] = Field(examples=['IN_PROGRESS'])
    create_date: str = Field(alias='createDate', examples=['2026-08-15'])