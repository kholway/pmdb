import os
import pytest
from sqlalchemy import text
from app.database import engine
from app.model import Base, Rating, Movie


def test_database_connection():
    engine.connect()

def test_movie_object():
    with pytest.raises(Exception) as e:
        mov = Movie()

    grail = Movie(
        title="Monty Python and the Holy Grail",
    )
    # Check types
    grail.runtime = "abc" # allowed, even though conflicts with type hint
    grail.runtime = "91"
    grail.mpaa_rating = "PG"  # allowed, even though conflicts with type hint
    grail.mpaa_rating = Rating.PG
    grail.director = "Terry Gilliam, Terry Jones"