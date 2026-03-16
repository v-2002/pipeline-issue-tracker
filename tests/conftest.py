import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import Base, get_db

# Use separate test database
TEST_DATABASE_URL = "sqlite:///./test_pipeline_tracker.db"

engine = create_engine(
    #TEST_DATABASE_URL — uses a separate SQLite database for tests. You never touch your real database during testing.
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db to use test database
#override_get_db() — replaces the real get_db with a test version that uses the test database. 
#This is FastAPI's dependency override system.
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#tells FastAPI: "whenever get_db is requested, use override_get_db instead"
app.dependency_overrides[get_db] = override_get_db

# creates the test client once for the entire test module, not once per test.
@pytest.fixture(scope="module")
def client():
    #creates all tables in test DB before tests run.
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    #drops all tables after tests complete, ensuring a clean slate for the next test run.
    Base.metadata.drop_all(bind=engine)