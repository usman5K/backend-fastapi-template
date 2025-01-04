from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

ALGORITHM = settings.JWT_ALGORITHM


def create_jwt_token(
    subject: str | Any,
    expire: int = None,
    extra_data: dict | None = None,
    refresh: bool = False,
) -> str:
    """
    Create a jwt token with the specified subject and optional extra data.

    :param expire: time in minutes after which the token expires. Must be an integer.
    :param subject: The subject of the token. Must be the primary key of the user in the database.
    :param extra_data: Optional data to include in the token. Must be a dictionary.
    :param refresh: Whether the token is a refresh token. Defaults to False. Must be a boolean.

    :return: The encoded jwt token.
    """
    current_datetime = datetime.now(timezone.utc)
    expire_time = (
        expire
        if expire
        else (
            current_datetime + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    )
    if refresh:
        expire_time = (
            expire
            if expire
            else (
                current_datetime
                + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
            )
        )

    payload = {
        "sub": str(subject),
        "refresh": refresh,
        "iat": current_datetime.timestamp(),
        "exp": expire_time.timestamp(),
    }
    if extra_data:
        payload.update({"extra": extra_data})

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the password against the hashed password.

    :param plain_password: The plain password to verify. Must be a string.
    :param hashed_password: The hashed password to compare against. Must be a string.

    :return: True if the password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash the password using the bcrypt algorithm.

    :param password: The password to hash. Must be a string.

    :return: The hashed password.
    """
    return pwd_context.hash(password)
