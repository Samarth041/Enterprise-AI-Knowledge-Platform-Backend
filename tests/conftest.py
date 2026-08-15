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



import uuid

@pytest.fixture
def auth_client(client):
    email = f"chat_test_{uuid.uuid4().hex}@example.com"

    signup_response = client.post(
        "/auth/signup",
        json={
            "name": "Chat Test User",
            "email": email,
            "password": "Test@123",
            "age": 21,
            "phone": "9727846321",
        },
    )

    assert signup_response.status_code in [200, 201]

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "Test@123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client