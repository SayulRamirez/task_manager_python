from sqlalchemy import exists, select

from dto.user_dto import LoginRequest, RegisterUser, UpdateUser
from models.user import User

from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, id: int):
        stmt = select(User).where(User.id == id)
        return self.db.execute(stmt).scalar_one_or_none()
    
    def exists_by_phone_number(self, phone_number: str) -> bool:
        stmt = select(exists().where(User.phone_number == phone_number))
        return bool(self.db.execute(stmt).scalar())
    
    def find_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()
    
    def update(self, id: int, request: UpdateUser):
        user = self.find_by_id(id)
        if not user:
            return None
        
        for key, value in request.model_dump(exclude_none=True).items():
            setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)

        return user

    def register(self, request: RegisterUser):
        user = User(**request.model_dump(exclude_none=True))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def login(self, request: LoginRequest) -> bool:
        stmt = select(exists().where(User.email == request.email,
                                     User.password == request.password))
        return bool(self.db.execute(stmt).scalar())
