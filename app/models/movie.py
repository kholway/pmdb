"""Defines the data model representing movies"""

from typing import Optional
import enum

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy.orm import Session
from app.database import engine, Base


class Rating(str, enum.Enum):
    G = "G"
    PG = "PG"
    PG13 = "PG-13"
    R = "R"
    NC17 = "NC-17"
    NR = "Not Rated"


class Movie(Base):
    __tablename__ = "Movie"
    
    id: Mapped[Optional[int]] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str]
    year: Mapped[Optional[int]]
    country: Mapped[Optional[str]]
    director: Mapped[Optional[str]]
    runtime: Mapped[Optional[int]]
    mpaa_rating: Mapped[Optional[Rating]] = mapped_column(Enum(Rating), default=None)

    def __repr__(self) -> str:
        return (f"Movie(id={self.id!r}, title={self.title!r}, " 
            f"year={self.year!r}, director={self.director!r}, "
            f"runtime={self.runtime!r}, mpaa_rating={self.mpaa_rating!r})"  
        )