from models.user import User, UserStatus


class UserRepository:
    __users: list[User] = []

    def __init__(self):
        pass

    def find_by_email_and_is_active(self, email: str) -> User | None:
        for user in self.__users:
            if user.email == email and user.status.value == UserStatus.ACTIVE.value:
                return user
        return None
    
    def exists_by_phone_number(self, phone_number: str) -> bool:
        for user in self.__users:
            if user.phone_number == phone_number:
                return True
        return False
    
    def find_by_email(self, email: str) -> User | None:
        for user in self.__users:
            if user.email == email:
                return user
        return None
