from fastapi import APIRouter, Depends, HTTPException, Path

from config.dependecies import get_project_service
from config.auth_depends import filter_token
from dto.project_dto import CreateProject, ProjectResponse
from models.project import Status
from service.project_service import ProjectService

from starlette import status

project_controller = APIRouter(prefix='/project', tags=['Project Controller'])

@project_controller.post(path='', response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, summary='Create new project')
async def create(user: filter_token, request: CreateProject, service: ProjectService = Depends(get_project_service)):
    return service.create_project(user.id, request)

@project_controller.get(path='/{id}', response_model=ProjectResponse, status_code=status.HTTP_200_OK, summary='Get project by id')
def get_project_by_id(user: filter_token, id: int = Path(gt=0), service: ProjectService = Depends(get_project_service)):
    response = service.get_project_by_id(id, user.id)

    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')
    return response

@project_controller.get(path='', response_model=list[ProjectResponse], status_code=status.HTTP_200_OK, summary='Get all projects by id leader')
def get_all_by_leader(user: filter_token, service: ProjectService = Depends(get_project_service)):
    return service.get_all_by_leader(user.id)

@project_controller.patch(path='/{id}/changed/{changed}', response_model=ProjectResponse, status_code=status.HTTP_200_OK, summary='Changed status project')
def changed_status(user: filter_token, id: int = Path(gt=0),
                   changed: Status = Path(description='El nuevo estado del proyecto'),
                   service: ProjectService = Depends(get_project_service)):
    response = service.changed_status(id, changed, user.id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')
    return response

@project_controller.delete(path='/{id}', status_code=status.HTTP_204_NO_CONTENT, summary='Deleted project')
def deleted(user: filter_token, id: int = Path(gt=0), service: ProjectService = Depends(get_project_service)):
    if not service.deleted(id, user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')