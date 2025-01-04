import logging
import time
from uuid import uuid4

import jwt
import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database
from testcontainers.postgres import PostgresContainer

from app.api.deps import SessionDep
from app.core.config import settings
from app.core.security import get_password_hash
from app.db.base_class import Base
from app.db.session import get_db
from app.main import app
from app.models import User

user_uuid_pk = uuid4()
postgres = PostgresContainer("postgres:16")
postgres.start()


@pytest.fixture(scope="session")
def db_engine():
    database_url = postgres.get_connection_url()
    alembic_cfg = Config()
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)
    alembic_cfg.set_main_option("script_location", "app/alembic")

    engine = create_engine(postgres.get_connection_url(), poolclass=StaticPool)

    with engine.begin() as connection:
        alembic_cfg.attributes["connection"] = connection
        command.upgrade(alembic_cfg, "head")

    yield engine
    Base.metadata.drop_all(bind=engine)
    drop_database(database_url)


@pytest.fixture(scope="module")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
    )()

    user = User()
    user.email = "test@dev.com"
    user.hashed_password = get_password_hash("test123")
    user.is_active = True
    user.id = user_uuid_pk

    session.add(user)
    session.commit()

    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[SessionDep] = override_get_db

    with TestClient(app) as client:
        yield client


JWT_ALGORITHM = settings.JWT_ALGORITHM or "HS256"
JWT_SECRET = settings.SECRET_KEY
TOKEN_EXPIRY_5_MINUTES_AS_SEC = 300


@pytest.fixture(scope="function")
def valid_auth_token() -> str:
    user_id = str(user_uuid_pk)
    payload = {"sub": user_id, "exp": time.time() + TOKEN_EXPIRY_5_MINUTES_AS_SEC}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


@pytest.fixture(scope="function")
def invalid_auth_token() -> str:
    user_id = str(uuid4())
    payload = {"sub": user_id, "exp": time.time() + TOKEN_EXPIRY_5_MINUTES_AS_SEC}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


@pytest.fixture(autouse=True, scope="module")
def disable_logger():
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)
