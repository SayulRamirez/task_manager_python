from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from config.dependecies import get_auth_service
from config.enviroment import get_env
from dto.user_dto import RegisterUser, UserResponse
from service.auth_service import AuthService

from starlette import status

IS_PROD = str(get_env('PROD')).lower() in ('1', 'true', 'yes')
TOKEN_EXPIRE = int(get_env('TOKEN_EXPIRE_SECONDS'))

auth_router = APIRouter(prefix='/auth', tags=['Auth Controller'])

@auth_router.post(path='/login', status_code=status.HTTP_200_OK, summary='Login app')
async def login(response: Response,
                request: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
                service: AuthService = Depends(get_auth_service)):

    auth_data = service.login(request.username, request.password)

    if not auth_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    response.set_cookie(
        key='access_token',
        value=f"{auth_data.get('access_token')}",
        max_age=TOKEN_EXPIRE,
        secure=IS_PROD,
        httponly=True,
        samesite='lax',
    )
    
    return {"message": "success login"}

@auth_router.post(path='/logout', status_code=status.HTTP_200_OK, summary="Close session")
async def logout(response: Response):
    response.delete_cookie(
        key='access_token',
        secure=IS_PROD,
        httponly=True,
        samesite='lax'
    )
    
    return {'message': 'Close session'}

@auth_router.post(path='/register', response_model=UserResponse, status_code=status.HTTP_200_OK, summary='Register new users')
async def register(request: RegisterUser, service: AuthService = Depends(get_auth_service)):
    response = service.register(request=request)

    if not response:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
    return response