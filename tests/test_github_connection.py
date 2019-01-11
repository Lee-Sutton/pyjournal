from unittest.mock import patch

import pytest

from pyjournal.github_connection import GithubConnection


@pytest.fixture
def mock_github_api():
    patcher = patch('pyjournal.github_connection.Github')
    yield patcher.start()
    patcher.stop()


@pytest.fixture()
def github_connection(mock_github_api, fake):
    username = fake.name()
    password = 'password'

    yield GithubConnection(username, password)


def test_github_connection(mock_github_api, fake):
    username = fake.name()
    password = 'password'

    GithubConnection(username, password)
    mock_github_api.assert_called_with(username, password)

def test_get_issues():
    pass
