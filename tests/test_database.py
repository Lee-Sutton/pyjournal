import os
from unittest.mock import patch


@patch('pyjournal.utils.makedirs_touch')
def test_database_initialization(makedirs_mock, tmpdir):
    """it should create the database connection based on the environment variable"""
    db_path = str(tmpdir.join('config.json'))
    os.environ['DB_PATH'] = db_path
    from pyjournal.database import db
    assert db.tables() is not None
    makedirs_mock.assert_called_with(db_path)

