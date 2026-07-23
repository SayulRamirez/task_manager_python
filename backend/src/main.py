from fastapi import FastAPI

from controller.user_controller import user_controller
from controller.auth_controller import auth_router
from controller.project_controller import project_controller

# from starlette.routing import BaseRoute


app = FastAPI(root_path='/api/v1', )
app.include_router(router=user_controller)
app.include_router(router=auth_router)
app.include_router(router=project_controller)