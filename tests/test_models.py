from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.movie import Rating, Movie
from app.models.movie import Base


@fixture
def mem_db():
    """Provide an in-memory database for testing"""
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    try:
        db = Session(engine)
        yield db
    finally:
        db.close()


@fixture
def movies():
    """Provide a list of movie objects for testing"""
    # Create movie objects
    grail = Movie(
        title="Monty Python and the Holy Grail",
        runtime=91,
        mpaa_rating = Rating.PG,
        director = "Terry Gilliam, Terry Jones"
    )
    brian = Movie(title="Monty Python's Life of Brian")
    meaning = Movie(title="Monty Python's The Meaning of Life")
    yield [grail, brian, meaning]
    # No teardown


def test_movie_object(movies):
    """Test behavior of movie object attributes"""
    grail = movies[0]

    assert grail.title == "Monty Python and the Holy Grail"
    assert grail.runtime == 91
    assert grail.mpaa_rating == Rating.PG
    assert grail.director == "Terry Gilliam, Terry Jones"


def test_create_movie(mem_db, movies):
    """Test that movie can be successfully added to the database"""
    # Check object before Create
    grail = movies[0]
    assert grail.id == None

    # Create
    mem_db.add(grail)
    mem_db.commit()
    
    # Check that movie added successfully
    grailid = mem_db.scalar(
        select(Movie.id)
        .where(Movie.title == "Monty Python and the Holy Grail")
    )
    assert grailid == 1
    
    # Check that object updated
    assert grail.id == 1


def test_read_movie():
    pass


def test_update_movie():
    pass


def test_delete_movie():
    pass