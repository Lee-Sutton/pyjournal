from os import path

import pytest
from click.testing import CliRunner
import faker
from faker.providers import internet

from pyjournal.db import models
from pyjournal.journal_commands import init


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture
def journal_test_dir(tmpdir):
    test_journal_path = path.join(tmpdir, 'Journal')
    yield test_journal_path


@pytest.fixture()
def test_db():
    """
    Creates a temporary transaction for testing and rolls back the database
    when the test completes
    """
    with models.DATABASE.transaction() as transaction:
        yield transaction
        transaction.rollback()


@pytest.fixture()
def initialized_db():
    """Initializes the database for testing purposes"""
    models.initialize_db()
    models.drop_db()
    yield
    models.drop_db()


@pytest.fixture()
def fake():
    """Returns instance of faker initialized with internet provider"""
    fake = faker.Faker()
    fake.add_provider(internet)
    yield fake


@pytest.fixture()
def initialized_journal(runner, journal_test_dir, test_db):
    """Returns an initialized instance of the database"""
    runner.invoke(init, args=['--path', journal_test_dir])
    yield test_db
