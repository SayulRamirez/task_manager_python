import datetime

import jwt

from config.enviroment import get_env

SECRET_KEY = get_env('SECRET_KEY')
ALGORITHM = get_env('ALGORITHM')

try:
    EXPIRE_MINUTES = int(get_env('TOKEN_EXPIRE_MINUTES'))
except ValueError:
    EXPIRE_MINUTES = 30

class JWTManager:

    @staticmethod
    def get_token(sub: str, user_id: int, extra_claims: dict | None = None) -> str:
        payload = {
            'sub': sub,
            'id': user_id,
        }

        expires = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=EXPIRE_MINUTES)
        payload.update({'exp': expires})

        if extra_claims:
            payload.update(extra_claims.copy())

        return jwt.encode(payload, SECRET_KEY, ALGORITHM)