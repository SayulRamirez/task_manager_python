from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from config.dependecies import get_user_repository
from config.jwt import JWTManager
from exceptions.auth import ForbiddenException, UnauthorizedUser
from models.user import Role, User
from repository.user_repository import UserRepository


oauth = OAuth2PasswordBearer(tokenUrl='/auth/login')
auth_depends = Annotated[str, Depends(oauth)]

async def get_current_user(token: auth_depends, user_repository: UserRepository = Depends(get_user_repository)):
    payload = JWTManager.decode_token(token)
    user_id: int = payload.get('id')

    if not user_id:
        raise UnauthorizedUser()
    
    user = user_repository.find_by_id(user_id)

    if not user or not user.is_active:
        raise UnauthorizedUser()
    
    return user

filter_token = Annotated[User, Depends(get_current_user)]


class RoleChecker:
    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, user: filter_token) -> User:
        if user.role not in self.allowed_roles:
            raise ForbiddenException()
        return user