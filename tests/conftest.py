from pytest import fixture
from tests.utils.db import setup_test_db, teardown_test_db
from app.models.movie import Rating

@fixture()
def mem_db():
    """Provide an in-memory database for testing"""
    engine, db = setup_test_db()
    yield db
    teardown_test_db(engine, db)


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