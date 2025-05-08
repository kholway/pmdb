from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.movie import Rating, Movie
from app.models.movie import Base
import sqlalchemy as sa


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
        year=1975,
        country="UK",
        director = "Terry Gilliam, Terry Jones",
        runtime=91,
        mpaa_rating = Rating.PG
    )
    brian = Movie(
        title="Monty Python's Life of Brian",
        year=1979,
        country="UK",
        director = "Terry Jones",
        runtime=94,
        mpaa_rating = Rating.R
    )
    meaning = Movie(
        title="Monty Python's Meaning of Life",
        year=1983,
        # omit country for testing ("UK, USA")
        director = "Terry Jones",
        runtime=107,
        mpaa_rating = Rating.R
    )
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


def test_read_movie(mem_db, movies):
    # Populate database first
    for mov in movies:
        mem_db.add(mov)
    mem_db.commit()

    # Try filtering on country of origin
    query = select(Movie.title).where(Movie.country == "UK")
    titles = mem_db.scalars(query).all()
    assert "Monty Python and the Holy Grail" in titles
    assert "Monty Python's Life of Brian" in titles
    assert "Monty Python's Meaning of Life" not in titles

    # Try sorting by movie run time
    query = select(Movie.title).order_by(sa.desc(Movie.runtime))
    titles = mem_db.scalars(query).all()
    assert len(titles) == 3
    assert titles == sorted([mov.title for mov in movies], reverse=True)


def test_update_movie():
    pass


def test_delete_movie():
    pass