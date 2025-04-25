from app.models.movie import Base, Rating, Movie

def test_movie_object():
    grail = Movie(
        title="Monty Python and the Holy Grail",
    )
    grail.runtime = 91 # would be nice for this to be converted to right type, as in Pydantic
    grail.mpaa_rating = Rating.PG
    grail.director = "Terry Gilliam, Terry Jones"
