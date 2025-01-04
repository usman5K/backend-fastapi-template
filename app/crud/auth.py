from pydantic import EmailStr

from app.api.deps import SessionDep
from app.core.security import verify_password
from app.crud.user import get_user_by_email
from app.models.user import User


def authenticate(session: SessionDep, email: EmailStr, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, str(db_user.hashed_password)):
        return None

    return db_user
