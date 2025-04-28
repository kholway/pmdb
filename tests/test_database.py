import pytest
from app.database import engine
from app.deps import get_db
from sqlalchemy import select

def test_database_connection():
    """Check that engine connects"""
    
    engine.connect()


def test_get_db():
    """Check basic functionality of the wiring"""

    gen = get_db()
    db = next(gen)

    assert db is not None
    
    print(db.execute(select(1)).all())
    
    with pytest.raises(Exception):
        next(gen)
    
    gen.close()