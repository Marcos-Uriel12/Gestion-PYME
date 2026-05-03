import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base, get_db
from app.main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client(db):
    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    
@pytest.fixture
def admin_token(client, db):
    from app.models.user import User
    from app.utils.password import hash_password
    
    session = TestingSessionLocal()
    admin = User(
        name="Admin",
        email="admin@admin.com",
        password=hash_password("admin123"),
        role="admin"
    )
    session.add(admin)
    session.commit()
    session.close()
    
    response = client.post("/auth/login", data={
        "username": "admin@admin.com",
        "password": "admin123"
    })
    return response.json()["access_token"]