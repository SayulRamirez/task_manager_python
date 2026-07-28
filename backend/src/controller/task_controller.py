
from fastapi import APIRouter, HTTPException

from dto.task_dto import CreateTask, TaskResponse
from service.task_service import TaskService

from starlette import status

task_controller = APIRouter(prefix='/task', tags=['Task Controller'])
task_service = TaskService()

@task_controller.post(path='', response_model=CreateTask, status_code=status.HTTP_201_CREATED, summary='Create a new task')
def create_task(self, request: CreateTask):
    response = task_service.create_task(request)
    if not response:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail='Project or user not found')
    return response

@task_controller.get(path='/{id}', response_model=TaskResponse, status_code=status.HTTP_200_OK, summary='Get task by id')
def get_task(self, id):
    response = task_service.get_task(id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    return response

@task_controller.get(path='/{id_responsible}/responsible', response_model=list[TaskResponse], status_code=status.HTTP_200_OK, summary='Get all task by id responsible')
def get_tasks_by_responsible(self, id_responsible):
    return task_service.get_tasks_by_responsible(id_responsible)

@task_controller.patch(path='/{id}/change/{change}', response_model=TaskResponse, status_code=status.HTTP_200_OK, summary='Changed status task')
def changed_status(self, id, change):
    response = task_service.changed_status(id, change)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    return response

@task_controller.delete(path='/{id}', status_code=status.HTTP_204_NO_CONTENT, summary='Deleted task')
def deleted(self, id):
    if not task_service.deleted(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')