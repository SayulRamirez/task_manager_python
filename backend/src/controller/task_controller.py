
from fastapi import APIRouter, Depends, HTTPException, Path

from config.dependecies import get_task_service
from dto.task_dto import CreateTask, TaskResponse
from models.project import Status
from service.task_service import TaskService

from starlette import status

task_controller = APIRouter(prefix='/task', tags=['Task Controller'])

@task_controller.post(path='', response_model=TaskResponse, status_code=status.HTTP_201_CREATED, summary='Create a new task')
def create_task(request: CreateTask, service: TaskService = Depends(get_task_service)):
    response = service.create_task(request)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project or user not found')
    return response

@task_controller.get(path='/{id}', response_model=TaskResponse, status_code=status.HTTP_200_OK, summary='Get task by id')
def get_task(id: int = Path(gt=0), service: TaskService = Depends(get_task_service)):
    response = service.get_task(id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    return response

@task_controller.get(path='/{id_responsible}/responsible', response_model=list[TaskResponse], status_code=status.HTTP_200_OK, summary='Get all task by id responsible')
def get_tasks_by_responsible(id_responsible: int = Path(gt=0), service: TaskService = Depends(get_task_service)):
    response = service.get_tasks_by_responsible(id_responsible)
    if len(response) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not foudn tasks wiht user')
    return response

@task_controller.patch(path='/{id}/change/{change}', response_model=TaskResponse, status_code=status.HTTP_200_OK, summary='Changed status task')
def changed_status(id: int = Path(gt=0),
                   change: Status = Path(description='El nuevo estado de la tarea'),
                   service: TaskService = Depends(get_task_service)):
    response = service.changed_status(id, change)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    return response

@task_controller.delete(path='/{id}', status_code=status.HTTP_204_NO_CONTENT, summary='Deleted task')
def deleted(id: int = Path(gt=0), service: TaskService = Depends(get_task_service)):
    if not service.deleted(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')