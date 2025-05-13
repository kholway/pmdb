from pytest import fixture
from tests.utils.db import setup_mem_db, teardown_db
from app.models.movie import Rating

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
        "mpaa_rating": Rating.PG
    }