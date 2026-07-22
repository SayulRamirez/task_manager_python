from enum import Enum


# class UserStatus(Enum):
#     ACTIVE = True
#     BLOCKED = False
#     DELETED = False

class Role(Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User:
    # def __init__(self, first_name: str, last_name: str, phone_number: str, email: str, password: str, maternal_surname: str = "", role: Role = Role.USER, status: UserStatus = UserStatus.ACTIVE):
    def __init__(self, id, first_name: str, last_name: str, phone_number: str, email: str, password: str, maternal_surname: str = "", role: Role = Role.USER):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.maternal_surname = maternal_surname
        self.role = role

    def update(self, fields):
        for key, value in fields.items():
            setattr(self, key, value)
