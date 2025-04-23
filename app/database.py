"""Manages the database connections"""

import logging

from sqlalchemy import create_engine


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
