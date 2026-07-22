from fastapi import APIRouter, Body, HTTPException, status, Path
from dto.user_dto import UpdateUser, UserResponse
from service.user_service import UserService


user_controller = APIRouter(prefix='/user', tags=['User controller'])
user_service = UserService()


@user_controller.get(path='/{id}', response_model=UserResponse, status_code=status.HTTP_200_OK, summary='Get information user', description='Get information user by id')
async def get_info(id: int = Path(gt=0)):
    response = user_service.get_info(id)
    if not response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")
    return response

@user_controller.patch(path='/{id}', response_model=UserResponse, status_code=status.HTTP_200_OK, summary='Change info user', description='Change info user by id')
async def update(id: int = Path(gt=0), request: UpdateUser = Body()):
    response = user_service.update_info(id, request)

    if not response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")
    return response

