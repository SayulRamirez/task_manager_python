from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.enviroment import get_env
from controller.user_controller import user_controller
from controller.auth_controller import auth_router
from controller.project_controller import project_controller
from controller.task_controller import task_controller

HOSTS = get_env('HOSTS')

origins = [host for host in HOSTS.split(',')]

app = FastAPI(root_path='/api/v1', )

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=user_controller)
app.include_router(router=auth_router)
app.include_router(router=project_controller)
app.include_router(router=task_controller)