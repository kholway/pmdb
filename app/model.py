from typing import Optional
import enum

from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import Mapped, mapped_column, relationship


# Create the model
#
class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Rating(enum.Enum):
    G = "G"
    PG = "PG"
    PG13 = "PG-13"
    R = "R"
    NC17 = "NC-17"
    NR = "Not Rated"


class Movie(Base):
    __tablename__ = "Movie"

    title: Mapped[str]
    
    id: Mapped[int] = mapped_column(primary_key=True, default=None)
    year: Mapped[Optional[int]] = mapped_column(default=None)
    director: Mapped[Optional[str]] = mapped_column(default=None)
    runtime: Mapped[Optional[int]] = mapped_column(default=None)
    mpaa_rating: Mapped[Optional[Rating]] = mapped_column(Enum(Rating), default=None)


def main():
    mov = Movie(title="Monty Python and the Holy Grail")
    mov.runtime = "abc" # Allowed, but conflicts with type hint
    print(mov)


if __name__ == "__main__":
    main()