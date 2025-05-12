import pytest
import sqlalchemy as sa
from sqlalchemy import select
import sqlalchemy.orm as sao

from app.models.movie import Base, Rating, Movie


@pytest.fixture
def mem_db():
    """Provide an in-memory database for testing"""
    engine = sa.create_engine("sqlite+pysqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    try:
        db = sao.Session(engine)
        yield db
    finally:
        db.close()


@pytest.fixture
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
    """Test movie model to ensure that movie can be successfully added to a database"""
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
    """Test movie model to ensure that movies can be successfully read from a database"""
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


def test_update_movie(mem_db, movies):
    """Test movie model to ensure that movies can be successfully updated in a database"""
    
    # Populate database first
    for mov in movies:
        mem_db.add(mov)
    mem_db.commit()

    # Update a movie
    meaning = mem_db.execute(
        select(Movie)
        .where(Movie.title == "Monty Python's Meaning of Life")
    ).scalar_one()
    assert isinstance(meaning, Movie)
    meaning.country = "UK, USA"
    assert meaning in mem_db.dirty
    
    # Check country not updated yet
    with mem_db.no_autoflush:
        meaning_country = mem_db.execute(
            select(Movie.country)
            .where(Movie.title == "Monty Python's Meaning of Life")
        ).scalar_one()
        assert meaning_country == None
    assert meaning in mem_db.dirty

    # Update DB and check country updated
    mem_db.commit()
    meaning_country = mem_db.execute(
        select(Movie.country)
        .where(Movie.title == "Monty Python's Meaning of Life")
    ).scalar_one()
    assert meaning_country == "UK, USA"
    assert meaning not in mem_db.dirty


def test_delete_movie(mem_db, movies):
    """Test movie model to ensure that movies can be successfully deleted from a database"""
    
    # Populate database first
    for mov in movies:
        mem_db.add(mov)
    mem_db.commit()
    
    # Pick a movie and delete it
    grail = mem_db.execute(
        select(Movie)
        .where(Movie.title == "Monty Python and the Holy Grail")
    ).scalar_one()
    assert isinstance(grail, Movie)
    mem_db.delete(grail)
    assert grail in mem_db.deleted

    # Check not updated yet
    with mem_db.no_autoflush:
        tmp = mem_db.execute(
            select(Movie)
            .where(Movie.title == "Monty Python and the Holy Grail")
        ).scalar_one()
        assert tmp is grail
    assert grail in mem_db.deleted
    
    # Update DB and check that delete was successful
    result = mem_db.execute(
        select(Movie)
        .where(Movie.title == "Monty Python and the Holy Grail")
    ).scalar_one_or_none()
    assert result is None
    assert grail not in mem_db.deleted