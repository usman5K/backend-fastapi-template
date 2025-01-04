from fastapi import APIRouter, status, Depends

from app.api.deps import get_current_user, SessionDep
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UpdateMe, UserPublic, UpdatePassword

routes = APIRouter(prefix="/user", tags=["User"])


@routes.get("", description="Get profile", status_code=status.HTTP_200_OK)
async def get_profile(current_user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.model_validate(current_user)


@routes.put("", description="Update profile", status_code=status.HTTP_200_OK)
async def update_me(
    session: SessionDep,
    user_in: UpdateMe,
    current_user: User = Depends(get_current_user),
) -> UserPublic:
    for key, value in user_in.model_dump().items():
        setattr(current_user, key, value)

    session.commit()
    return UserPublic.model_validate(current_user)


@routes.put(
    "/reset-password",
    description="Update user password",
    status_code=status.HTTP_200_OK,
)
async def reset_password(
    session: SessionDep,
    user_in: UpdatePassword,
    current_user: User = Depends(get_current_user),
) -> UserPublic:
    hashed_password = get_password_hash(user_in.new_password)
    current_user.hashed_password = hashed_password
    session.commit()

    return UserPublic.model_validate(current_user)


@routes.delete("", description="Delete user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
) -> None:
    session.delete(current_user)
    session.commit()
