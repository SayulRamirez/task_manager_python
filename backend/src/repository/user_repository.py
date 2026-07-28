from dto.user_dto import LoginRequest, RegisterUser, UpdateUser
from models.user import User

from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, id: int):
        return self.db.query(User).filter(User.id == id).first()
    
    def exists_by_phone_number(self, phone_number: str) -> bool:
        return self.db.query(User).filter(User.phone_number == phone_number).first() is not None
    
    def find_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
    
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
    
    def login(self, request: LoginRequest):
        user = self.db.query(User).filter(
            User.email == request.email,
            User.password == request.password
        ).first
        return user is not None
