from typing import Literal

from fastapi import APIRouter, HTTPException, Path

from dto.project_dto import CreateProject, ProjectResponse
from service.project_service import ProjectService

from starlette import status

project_controller = APIRouter(prefix='/project', tags=['Project Controller'])
project_service = ProjectService()

@project_controller.post(path='', response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, summary='Create new project')
async def create(request: CreateProject):
    response = project_service.create_project(request)

    if not response:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden create project')
    return response

@project_controller.get(path='/{id}', response_model=ProjectResponse, status_code=status.HTTP_200_OK, summary='Get project by id')
def get_project_by_id(id: int = Path(gt=0)):
    response = project_service.get_project_by_id(id)

    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')
    return response

@project_controller.get(path='/{id}/leader', response_model=list[ProjectResponse], status_code=status.HTTP_200_OK, summary='Get all projects by id leader')
def get_all_by_leader(id_leader: int = Path(gt=0)):
    response = project_service.get_all_by_leader(id_leader)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found with leader id')
    return response

@project_controller.get(path='/{id}/changed/{changed}', response_model=ProjectResponse, status_code=status.HTTP_200_OK, summary='Changed status project')
def changed_status(id: int = Path(gt=0), changed: Literal['PENDING', 'IN_PROGRESS', 'COMPLETE'] = Path()):
    response = project_service.changed_status(id, changed)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')
    return response

@project_controller.get(path='/{id}', status_code=status.HTTP_204_NO_CONTENT, summary='Deleted project')
def deleted(id: int = Path(gt=0)):
    response = project_service.deleted(id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')