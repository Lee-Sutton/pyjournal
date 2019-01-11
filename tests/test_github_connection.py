from unittest.mock import patch

import pytest

from pyjournal.github_connection import GithubConnection


@pytest.fixture
def mock_github_api():
    patcher = patch('pyjournal.github_connection.Github')
    yield patcher.start()
    patcher.stop()


def test_github_connection(mock_github_api, fake):
    username = fake.name()
    password = 'password'

    GithubConnection(username, password)
    mock_github_api.assert_called_with(username, password)


def test_get_prs_awaiting_review(mock_github_api, fake):
    """It should return a list of issues awaiting review"""
    username = fake.name()
    password = 'password'

    github_connection = GithubConnection(username, password)
    github_connection.get_prs_awaiting_review()
    mock_github_api().search_issues.assert_called_with(
        f'is:open is:pr review-requested:{username}')
