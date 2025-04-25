import pytest
from app.database import engine


def test_database_connection():
    engine.connect()