from dto.user_dto import LoginRequest, RegisterUser
from repository.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, request: LoginRequest):
        if self.user_repository.login(request):
            return { 'token': 'secret_token' }
        return None

    def register(self, request: RegisterUser):
        if self.user_repository.find_by_email(request.email):
            return None
        
        return self.user_repository.register(request)