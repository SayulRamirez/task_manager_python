from fastapi import APIRouter, HTTPException

from dto.user_dto import AuthResponse, LoginRequest, RegisterUser, UserResponse
from service.auth_service import AuthService

from starlette import status

auth_router = APIRouter(prefix='/auth', tags=['Auth Controller'])
auth_service = AuthService()

@auth_router.post(path='/login', response_model=AuthResponse, status_code=status.HTTP_200_OK, summary='Login de la app')
async def login(request: LoginRequest):
    response = auth_service.login(request=request)

    if not response:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return response

@auth_router.post(path='/register', response_model=UserResponse, status_code=status.HTTP_200_OK, summary='Register new users')
async def register(request: RegisterUser):
    response = auth_service.register(request=request)

    if not response:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
    return response
