import os
import pytest
from sqlalchemy import text
from app.database import engine

def test_database_connection():
    engine.connect()
