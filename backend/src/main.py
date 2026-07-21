from fastapi import FastAPI

from controller.user_controller import user_controller


app = FastAPI(root_path='/api/v1')
app.include_router(router=user_controller)