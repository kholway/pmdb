import sqlalchemy as sa
import sqlalchemy.orm as sao
from app.models.movie import Base


def setup_test_db() -> tuple[sa.engine.base.Engine, sao.Session]:    
    """Provide an in-memory database for testing"""
    engine = sa.create_engine("sqlite+pysqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    db = sao.Session(engine)
    return engine, db


def teardown_test_db(engine: sa.engine.base.Engine, db: sao.Session):
    """Tear down the in-memory database"""
    db.close()
    engine.dispose()