from app.core import security
from app.models.user import User
from app.schemas.common import Token


def generate_token_response_data(user: User) -> Token:
    extra_data = {"email": user.email}

    return Token(
        access_token=security.create_jwt_token(subject=user.id, extra_data=extra_data),
        refresh_token=security.create_jwt_token(
            subject=user.id, extra_data=extra_data, refresh=True
        ),
    )
