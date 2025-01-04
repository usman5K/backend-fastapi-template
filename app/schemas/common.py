import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator

from app.core.config import settings
from app.schemas.user import UserPublic


class RefreshTokenRequest(BaseModel):
    access_token: str
    refresh_token: str

    @classmethod
    @field_validator("refresh_token")
    def validate_refresh_token(cls, refresh_token):
        # decode refresh token and validate refresh key in payload
        try:
            decoded_refresh_token = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            if not decoded_refresh_token.get("refresh"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid refresh token",
                )
            return refresh_token
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token has expired",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token"
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token"
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong",
            )


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    refresh_token: str | None
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: str | None = None


# Generic message
class Message(BaseModel):
    message: str


class AuthResponse(BaseModel):
    token: Token
    user: UserPublic
