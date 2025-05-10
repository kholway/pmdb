from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.movie import MovieCreate, MovieResponse
from app.models.movie import Movie
from app.deps import get_db


router = APIRouter()


@router.post("/movies/", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)) -> Movie:
    """Adds a movie to the database and returns the orm"""

    new_movie = Movie(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie