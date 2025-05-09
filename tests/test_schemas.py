import pytest
import pydantic
from app.schemas import MovieBase, MovieCreate, MovieResponse
from app.models.movie import Rating, Movie


def test_movie_create_valid():
    """Test that a movie can be created."""

    data = {
        "title": "Monty Python and the Holy Grail",
        "director": "Terry Gilliam, Terry Jones",
        "runtime": 91,
        "year": 1975,
        "country": "UK",
        "mpaa_rating": Rating.PG
    }
    movie = MovieCreate(**data)
    assert movie.title == data["title"]
    assert movie.year == data["year"]
    assert movie.country == data["country"]
    assert movie.director == data["director"]
    assert movie.runtime == data["runtime"]
    assert movie.mpaa_rating == data["mpaa_rating"]
    

def test_movie_create_missing_required_field():
    """Test that a movie creation fails if a required field is missing."""

    data = {"year": 1975}
    with pytest.raises(pydantic.ValidationError) as e:
        movie = MovieCreate(**data)


def test_movie_create_optional_fields():
    """Test that optional fields are handled correctly."""

    data = {"title": "Monty Python and the Holy Grail"}
    movie = MovieCreate(**data)
    assert movie.title is data["title"]
    assert movie.year is None
    assert movie.country is None
    assert movie.director is None
    assert movie.runtime is None
    assert movie.mpaa_rating is None


def test_movie_create_extra_data():
    """Test that extraneous data is ignored"""

    data = {
        "title": "Monty Python and the Holy Grail",
        "foo": "bar"
    }    
    movie = MovieCreate(**data)
    assert movie.title is data["title"]
    with pytest.raises(Exception):
        movie.foo
    

def test_movie_base_invalid_year():
    """Test that invalid year values raise validation errors."""

    data = {
    "title": "Monty Python and the Holy Grail",
    "year": -1975,
    }
    with pytest.raises(pydantic.ValidationError):
        MovieCreate(**data)

        
def test_movie_response_from_orm():
    """Test that an ORM object can be validated."""

    grail_orm = Movie(
        id=1, # for testing, provide this explicitly
        title="Monty Python and the Holy Grail",
        year=1975,
        country="UK",
        director = "Terry Gilliam, Terry Jones",
        runtime=91,
        mpaa_rating = Rating.PG
    )
    
    grail_model = MovieResponse.model_validate(grail_orm)
    

def test_movie_response_data_serialization():
    """Test that the response serializes correctly."""
     
    data = {
        "title": "Monty Python and the Holy Grail",
        "director": "Terry Gilliam, Terry Jones",
        "runtime": 91,
        "year": 1975,
        "country": "UK",
        "mpaa_rating": Rating.PG
    }
    movie = MovieResponse(id=1,**data)
    dump = movie.model_dump()
    assert isinstance(dump, dict)
    assert dump["title"] == data["title"]
    assert dump["runtime"] == data["runtime"]
    


def test_movie_response_schema_serialization():
    """Test that the response schema serializes correctly."""
    # Not sure what this is yet
    pass