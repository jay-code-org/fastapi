from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .config import settings as config


aouth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    payload = data.copy()
    token_expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=int(config.jwt_expires_minutes)
    )
    payload.update({"exp": token_expire_time})

    jwt_encoded = jwt.encode(
        payload, config.jwt_secret_key, algorithm=config.jwt_algorithm
    )

    return jwt_encoded


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, config.jwt_secret_key, config.jwt_algorithm)

        if payload.get("id") is None or payload.get("sub") is None:
            raise credentials_exception

        token_data = schemas.TokenData(sub=payload.get("sub"), id=payload.get("id"))
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(aouth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Unauthorized access",
        headers={"WWW-Authenticage": "Bearer"},
    )

    return verify_access_token(token, credentials_exception)
