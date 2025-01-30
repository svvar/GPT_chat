import os
from datetime import datetime, timedelta, UTC

import jwt
from dotenv import load_dotenv, find_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Cookie

from app.schemas.user import UserPublic

load_dotenv(find_dotenv())

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неправильні дані облікового запису",
    headers={"WWW-Authenticate": "Bearer"},
)

expired_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Час сесії вичерпався",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(access_token: str = Cookie(None)) -> UserPublic | None:
    if not access_token:
        return None

    token = access_token.replace("Bearer ", "").strip()

    payload = decode_access_token(token)
    login = payload.get("login")
    user_id = payload.get("id")
    if login is None:
        raise credentials_exception
    return UserPublic(login=login, id=user_id)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
        return payload if payload else None
    except jwt.ExpiredSignatureError:
        raise expired_exception
    except jwt.PyJWTError:
        raise credentials_exception




