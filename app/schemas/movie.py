from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from app.models.movie import Rating

class MovieBase(BaseModel):
    """The Pydantic model representing a Movie"""
    title: str
    year: Optional[int] = Field(None, gt=1900, lt=datetime.now().year+10)
    country: Optional[str] = None
    director: Optional[str] = None
    runtime: Optional[int] = None
    mpaa_rating: Optional[Rating] = None


class MovieCreate(MovieBase):
    """The Pydantic model responsible for movie creation"""
    pass


class MovieUpdate(MovieBase):
    """The Pydantic model responsible for movie updates"""
    pass


class MovieResponse(MovieBase):
    """The Pydantic model responsible for movie reading"""
    # Modern placement for orm_mode = True
    model_config = ConfigDict(from_attributes=True)

    id: int