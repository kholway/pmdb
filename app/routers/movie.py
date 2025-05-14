import logging
import logging.config
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from app.schemas.movie import MovieCreate, MovieUpdate, MovieResponse
from app.models.movie import Movie
from app.deps import get_db


logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

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


@router.get(
        "/movies/{movie_id}", response_model=MovieResponse,
        name="read_movie")
def read_movie(movie_id: int, db: Session = Depends(get_db)) -> Movie:
    """Read a movie from the database using its id"""

    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.put("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int,
                 movie_update: MovieUpdate, 
                 db: Session = Depends(get_db)) -> Movie:
    """Update a movie given using its id"""
    
    logger.debug(f"Starting update movie with movie_update: {movie_update.model_dump_json()}")

    # Fetch movie
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Overwrite all fields
    for field, value in movie_update.model_dump().items():
        setattr(movie, field, value)

    db.commit()
    db.refresh(movie)
    return movie