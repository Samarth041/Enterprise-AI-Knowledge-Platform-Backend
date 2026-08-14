import pytest 
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app

from app.db.database import Base, get_db

TEST_DATABASE_URL="sqlite:///./enterprise_test.db"

test_engine=create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread":False}
)

TestingSessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

@pytest.fixture(scope="session",autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db]=override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

