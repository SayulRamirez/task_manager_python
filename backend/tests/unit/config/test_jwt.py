import datetime
import pytest
import jwt
from fastapi import HTTPException
from config.jwt import JWTManager, SECRET_KEY, ALGORITHM
from exceptions.auth import UnauthorizedUser


def test_jwt_manager_get_and_decode_token_success():
    # Arrange & Act
    token = JWTManager.get_token(sub="user@example.com", user_id=1, extra_claims={"role": "ADMIN"})
    payload = JWTManager.decode_token(token)

    # Assert
    assert payload["sub"] == "user@example.com"
    assert payload["id"] == 1
    assert payload["role"] == "ADMIN"


def test_jwt_manager_decode_expired_token():
    # Generar un token con exp en el pasado (-10 minutos)
    past_expires = datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=10)
    expired_payload = {"sub": "user@example.com", "id": 1, "exp": past_expires}
    expired_token = jwt.encode(expired_payload, SECRET_KEY, ALGORITHM)

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        JWTManager.decode_token(expired_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Expired token"


def test_jwt_manager_decode_invalid_token():
    with pytest.raises(UnauthorizedUser):
        JWTManager.decode_token("token_invalido_o_malformado")