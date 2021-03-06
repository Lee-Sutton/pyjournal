import os
from os import path

import pytest
from click.testing import CliRunner
import faker
from faker.providers import internet

from pyjournal.database import initialize_database


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture
def journal_test_dir(tmpdir):
    test_journal_path = path.join(tmpdir, 'Journal')
    yield test_journal_path


@pytest.fixture()
def test_db(tmpdir):
    """creates a temporary database for testing"""
    os.environ['DB_PATH'] = str(tmpdir.join('config.json'))
    yield initialize_database()
    os.environ.pop('DB_PATH')


@pytest.fixture()
def fake():
    """Returns instance of faker initialized with internet provider"""
    fake = faker.Faker()
    fake.add_provider(internet)
    yield fake
