from pydantic import EmailStr

from app.api.deps import SessionDep
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserRegister


def get_user_by_email(session: SessionDep, email: EmailStr) -> User | None:
    user = session.query(User).filter_by(email=email).first()
    return user


def create_user(session: SessionDep, user_create: UserRegister):
    hashed_password = get_password_hash(user_create.password)
    user_data = user_create.model_dump()

    user = User()
    user.email = user_data["email"]
    user.hashed_password = hashed_password
    user.username = user_data.get("username")
    user.first_name = user_data.get("first_name")
    user.last_name = user_data.get("last_name")
    # user.profile_picture = user_data.get('profile_picture')
    user.bio = user_data.get("bio")

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
