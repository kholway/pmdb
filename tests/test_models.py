import sqlalchemy as sa
from sqlalchemy import select

from app.models.movie import Rating, Movie


def test_movie_object(movie_data):
    """Test behavior of movie object attributes"""
    grail = Movie(**movie_data)
    grail.mpaa_rating = Rating.PG

    assert grail.title == "Monty Python and the Holy Grail"
    assert grail.runtime == 91
    assert grail.mpaa_rating == Rating.PG
    assert grail.director == "Terry Gilliam, Terry Jones"


def test_create_movie(mem_db, movie_data):
    """Test movie model to ensure that movie can be successfully added to a database"""
    # Check object before Create
    grail = Movie(**movie_data)
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


def test_read_movie(mem_db, movie_data):
    """Test movie model to ensure that movies can be successfully read from a database"""
    # Populate database first
    brian_data = {
        "title": "Monty Python's Life of Brian",
        "year": 1979,
        "country": "UK",
        "director": "Terry Jones",
        "runtime": 94,
        "mpaa_rating": "R"
    }
    meaning_data = {
        "title": "Monty Python's Meaning of Life",
        "year": 1983,
        # omit country for testing ("UK, USA")
        "director": "Terry Jones",
        "runtime": 107,
        "mpaa_rating": "R"
    }
    
    movies = [
        Movie(**movie_data),
        Movie(**brian_data),
        Movie(**meaning_data)
    ]
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


def test_update_movie(mem_db, movie_data):
    """Test movie model to ensure that movies can be successfully updated in a database"""
    
    # Populate database first
    mov = Movie(**movie_data)
    mem_db.add(mov)
    mem_db.commit()

    # Update a movie
    grail = mem_db.execute(
        select(Movie)
        .where(Movie.title == movie_data["title"])
    ).scalar_one()
    assert isinstance(grail, Movie)
    grail.country = "USA"
    assert grail in mem_db.dirty
    
    # Check country not updated yet
    with mem_db.no_autoflush:
        grail_country = mem_db.execute(
            select(Movie.country)
            .where(Movie.title == movie_data["title"])
        ).scalar_one()
        assert grail_country == "UK"
    assert grail in mem_db.dirty

    # Update DB and check country updated
    mem_db.commit()
    grail_country = mem_db.execute(
        select(Movie.country)
        .where(Movie.title == movie_data["title"])
    ).scalar_one()
    assert grail_country == "USA"
    assert grail not in mem_db.dirty


def test_delete_movie(mem_db, movie_data):
    """Test movie model to ensure that movies can be successfully deleted from a database"""
    grail_title = movie_data["title"]

    # Populate database first
    grail = Movie(**movie_data)
    mem_db.add(grail)
    mem_db.commit()
    
    # Pick a movie and delete it
    grail = mem_db.execute(
        select(Movie)
        .where(Movie.title == grail_title)
    ).scalar_one()
    assert isinstance(grail, Movie)
    mem_db.delete(grail)
    assert grail in mem_db.deleted

    # Check not updated yet
    with mem_db.no_autoflush:
        tmp = mem_db.execute(
            select(Movie)
            .where(Movie.title == grail_title)
        ).scalar_one()
        assert tmp is grail
    assert grail in mem_db.deleted
    
    # Update DB and check that delete was successful
    result = mem_db.execute(
        select(Movie)
        .where(Movie.title == grail_title)
    ).scalar_one_or_none()
    assert result is None
    assert grail not in mem_db.deleted