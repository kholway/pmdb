from pytest import fixture
from fastapi.testclient import TestClient

from tests.utils.db import setup_mem_db, teardown_db
from app.models.movie import Rating
from app.main import app
from app.deps import get_db


@fixture()
def mem_db():
    """Provide an in-memory database for testing"""
    engine, SessionLocal = setup_mem_db()
    db = SessionLocal()
    yield db
    db.close()
    teardown_db(engine)


@fixture()
def movie_data():
    """Provide a default movie for testing"""
    yield {
        "title": "Monty Python and the Holy Grail",
        "year": 1975,
        "country": "UK",
        "director": "Terry Gilliam, Terry Jones",
        "runtime": 91,
    }


@fixture()
def client(mem_db):
    def override_get_db():
        yield mem_db
        
    # Setup
    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)

    # Provide the test client
    yield test_client

    # Cleanup
    app.dependency_overrides.clear()