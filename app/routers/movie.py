from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.schemas.movie import MovieCreate, MovieResponse
from app.models.movie import Movie
from app.deps import get_db


router = APIRouter()


@router.post("/movies/", response_model=MovieResponse, status_code=201)
def create_movie(
        movie: MovieCreate, response: Response,
        db: Session = Depends(get_db)) -> Movie:
    """Adds a movie to the database and returns the orm"""

    new_movie = Movie(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie) # necessary??

    # Add headers
    response.headers["Location"] = f"/movies/{new_movie.id}"

    return new_movie