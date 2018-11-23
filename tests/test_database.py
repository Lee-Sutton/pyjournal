import os
from pyjournal.database import initialize_database


def test_database_initialization(tmpdir):
    """it should create the database connection based on the environment variable"""
    db_path = str(tmpdir.join('config.json'))
    os.environ['DB_PATH'] = db_path
    db = initialize_database()
    assert db.tables() is not None
    assert os.path.exists(db_path)

