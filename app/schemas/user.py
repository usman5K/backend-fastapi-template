import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class UserBase(BaseModel):
    username: str | None
    email: EmailStr
    is_active: bool
    is_superuser: bool
    first_name: str | None
    last_name: str | None
    last_login_at: datetime | None
    profile_picture: str | None
    bio: str | None


class UpdateMe(BaseModel):
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = None
    profile_picture: str | None = None
    bio: str | None = None
    username: str | None = None


class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

    @classmethod
    @field_validator("new_password")
    def validate_passwords(cls, new_password, values):
        # Check if old_password exists and is not the same as new_password
        old_password = values.get("old_password")
        if old_password and new_password and old_password == new_password:
            raise ValueError("New password must not be the same as the old password.")

        return new_password


class UserPublic(UserBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class UserRegister(BaseModel):
    username: str | None = None
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    # profile_picture: str | None
    bio: str | None = None


class UserLogin(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
