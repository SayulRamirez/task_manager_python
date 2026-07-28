from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProjectBase(BaseModel):
    title: str = Field(min_length=3, max_length=25, examples=['Proyecto 1'])
    description: str = Field(min_length=3, max_length=100, examples=['Descripción del Proyecto 1'])
    estimated_completion: date = Field(alias='estimateCompletion', examples=['2026-07-02'])

    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        #populate_by_name=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

class CreateProject(ProjectBase):
    leader: int = Field(gt=0, examples=[1])

    @field_validator('estimated_completion')
    @classmethod
    def validate_feature_date(cls, value: date):
        if value < date.today():
            raise ValueError('La fecha estimada no puede estar en el pasado')
        return value

class ProjectResponse(ProjectBase):
    id: int = Field(gt=0, examples=[4])
    status: Literal['COMPLETE', 'IN_PROGRESS', 'PENDING'] = Field(examples=['IN_PROGRESS'])

    model_config = ConfigDict(from_attributes=True)