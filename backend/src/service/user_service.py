from fastapi import HTTPException
from starlette import status

from dto.user_dto import UpdateUser
from repository.user_repository import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_info(self, id: int):
        return self.user_repository.find_by_id(id)
    
    def update_info(self, id: int, request: UpdateUser):        
        return self.user_repository.update(id, request)
    
    # def changed_status(self, id, request: Status):
    #     user = self.user_repository.find_by_id(id)

    #     if not user:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")
        
    #     return self.user_repository.changed_status(id, request)