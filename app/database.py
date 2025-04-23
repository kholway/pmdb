"""Manages the database connections"""

import logging
from typing import Optional
import enum

from sqlalchemy import create_engine
from sqlalchemy import Enum
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import Mapped, mapped_column, relationship


# Set up logging
#
if __name__ == '__main__':
    logging.basicConfig(
        filename='database.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)


# Set up engine
#
db_type = "sqlite"
db_api = "pysqlite"
db_name = "movies.db"
db_url = f"{db_type}+{db_api}:///./{db_name}"
should_echo = True
logger.debug(f"Setting up database engine... {db_url}")
engine = create_engine(db_url, echo=should_echo)


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