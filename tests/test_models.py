from app.models.movie import Base, Rating, Movie

def test_movie_object():
    grail = Movie(
        title="Monty Python and the Holy Grail",
    )
    # Check types
    grail.runtime = "abc" # allowed, even though conflicts with type hint
    grail.runtime = "91" # would be nice for this to be converted to right type, as in Pydantic
    grail.mpaa_rating = "PG"  # allowed, even though conflicts with type hint
    grail.mpaa_rating = Rating.PG
    grail.director = "Terry Gilliam, Terry Jones"