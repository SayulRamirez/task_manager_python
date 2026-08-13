
from typing import Any, Mapping

from fastapi import HTTPException
from starlette import status

class UnauthorizedUser(HTTPException):
    def __init__(self, status_code: int = status.HTTP_401_UNAUTHORIZED,
                 detail: Any = 'Credentials not valid',
                 headers: Mapping[str, str] | None = {'WWW-Authenticate': 'Bearer'}) -> None:
        super().__init__(status_code, detail, headers)
