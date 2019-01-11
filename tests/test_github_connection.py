from pyjournal.github_connection import GithubConnection
from unittest.mock import patch


@patch('pyjournal.github_connection.Github')
def test_github_connection(mock_github_api, fake):
    username = fake.name()
    password = 'password'

    GithubConnection(username, password)
    mock_github_api.assert_called_with(username, password)


