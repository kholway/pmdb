from typing import Optional
import enum

from sqlmodel import Field, SQLModel, Session
from sqlalchemy import Column
from sqlalchemy import Enum
# from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
# from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import engine


# Create the model
#
# class Base(MappedAsDataclass, DeclarativeBase):
#     pass


class Rating(enum.Enum):
    G = "G"
    PG = "PG"
    PG13 = "PG-13"
    R = "R"
    NC17 = "NC-17"
    NR = "Not Rated"


class Movie(SQLModel, table=True):
    # __tablename__ = "Movie"

    id: Optional[int] = Field(primary_key=True, default=None)
    title: str
    year: Optional[int] = None
    director: Optional[str] = None
    runtime: Optional[int] = None
     # This doesn't actually generate an enum data type for the database, but SQLite doesn't have enums anyway
    mpaa_rating: Optional[Rating] = Field(sa_column=Column(Enum(Rating)), default=None)
    

def main():
    SQLModel.metadata.create_all(engine)
    
    mov = Movie(title="Monty Python and the Holy Grail")
    mov.runtime = 91
    
    with Session(engine) as session:
        session.add(mov)
        session.commit()


if __name__ == "__main__":
    main()