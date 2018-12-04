"""Jira connection test suite"""
from pyjournal.jira_connection import jira
from unittest.mock import patch


@patch('pyjournal.jira_connection.JIRA')
def test_jira_cli(mock_jira, runner, test_db):
    """It should allow the user to initialize their jira settings"""
    # The user wants to initialize their jira connection
    url = 'dummy_url'
    email = 'lee@e.com'
    password = '123456'

    result = runner.invoke(jira, args=['--init'], input=f'{url}\n{email}\n{password}\n')
    assert result.exit_code == 0

    mock_jira.assert_called_with(url, auth=(email, password))
    # assert 'Jira connection successful' in result.output


