import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=False, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=True)  # Nullable for SSO users
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login_at = Column(DateTime, nullable=True)  # Last login time

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)  # URL to profile picture
    bio = Column(String, nullable=True)  # Short biography or description

    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    auth_provider_token = relationship("UserAuthProviderToken", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class UserAuthProviderToken(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    provider_name = Column(
        String, nullable=False
    )  # e.g., 'google', 'facebook', 'twitter', 'form'
    access_token = Column(String, nullable=False)
    refresh_token = Column(
        String, nullable=True
    )  # Nullable if the provider does not use refresh tokens
    expires_at = Column(DateTime, nullable=True)  # Token expiration time

    # Relationship
    user = relationship("User", back_populates="auth_provider_token")

    def __repr__(self):
        return f"<UserAuthToken(user_id={self.user_id}, provider_name={self.provider_name})>"
