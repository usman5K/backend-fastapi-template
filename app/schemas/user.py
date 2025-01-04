import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator


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

    @model_validator(mode="before")
    def validate_passwords(self):
        # Check if current_password is not the same as new_password
        current_password = self.get("current_password")
        new_password = self.get("new_password")
        if current_password and new_password and current_password == new_password:
            raise ValueError(
                "New password must not be the same as the current password."
            )

        return self


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
