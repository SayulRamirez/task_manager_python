import datetime

from fastapi import HTTPException
from starlette import status
import jwt

from config.enviroment import get_env
from exceptions.auth import UnauthorizedUser

SECRET_KEY = get_env('SECRET_KEY')
ALGORITHM = get_env('ALGORITHM')

try:
    EXPIRE_SECONDS = int(get_env('TOKEN_EXPIRE_SECONDS'))
except ValueError:
    EXPIRE_SECONDS = 3600

class JWTManager:

    @staticmethod
    def get_token(sub: str, user_id: int, extra_claims: dict | None = None) -> str:
        payload = {
            'sub': sub,
            'id': user_id,
        }

        expires = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=EXPIRE_SECONDS)
        payload.update({'exp': expires})

        if extra_claims:
            payload.update(extra_claims.copy())

        return jwt.encode(payload, SECRET_KEY, ALGORITHM)
    
    @staticmethod
    def decode_token(token: str):
        try:
            return jwt.decode(token, SECRET_KEY, [ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Expired token')
        except jwt.InvalidTokenError:
            raise UnauthorizedUser()