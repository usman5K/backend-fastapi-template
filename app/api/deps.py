from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError, InvalidSignatureError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.core.logger import logger
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import TokenPayload

reusable_oauth2 = HTTPBearer()
SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[HTTPAuthorizationCredentials, Depends(reusable_oauth2)]


def get_auth_token(token_data: TokenDep) -> str:
    return token_data.credentials


def get_current_user(
    session: SessionDep, token: str = Depends(get_auth_token)
) -> User():
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        if payload.get("refresh"):
            logger.warning(
                "Access attempt with refresh token",
                extra={"user_id": payload.get("sub")},
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid access token"
            )

        token_data = TokenPayload(**payload)

    except (ExpiredSignatureError, InvalidSignatureError, ValidationError) as e:
        logger.error(f"Token validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        logger.warning("Inactive user access attempt")
        raise HTTPException(status_code=400, detail="Inactive user")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        logger.warning(
            f"Unauthorized superuser access attempt by user: {current_user.id}"
        )
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
