import logging
import logging.config
import sqlalchemy as sa
import sqlalchemy.orm as sao
from app.models.movie import Base

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

def setup_mem_db() -> tuple[sa.engine.base.Engine, sao.sessionmaker]:    
    """Provide an in-memory database for testing"""
    engine = sa.create_engine("sqlite+pysqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    logger.debug("Created in-memory database tables!")
    SessionLocal = sao.sessionmaker(engine)
    return engine, SessionLocal


def teardown_db(engine: sa.engine.base.Engine):
    """Tear down the in-memory database"""
    engine.dispose()