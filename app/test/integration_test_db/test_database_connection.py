import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.configuration.database import engine


def test_database_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar_one() == 1
    except OperationalError as e:
        pytest.fail(f"Could not connect to the database: {e}")
