"""Jira connection test suite"""
from pyjournal.jira_connection import jira
from unittest.mock import patch
from tinydb import Query


@patch('pyjournal.jira_connection')
def test_jira_cli(mock_jira, runner, test_db):
    """It should allow the user to initialize their jira settings"""
    # The user wants to initialize their jira connection
    url = 'dummy_url'
    email = 'lee@e.com'
    password = '123456'

    result = runner.invoke(jira, args=['--init'], input=f'{url}\n{email}\n{password}\n')
    assert result.exit_code == 0

    mock_jira.assert_called_with(url, auth=(email, password))

    # The data should be stored in the database
    config = test_db.get(Query().jira.exists())
    jira_config = config['jira']
    assert jira_config is not None
    assert jira_config['url'] == url
    assert jira_config['email'] == email
    assert jira_config['password'] == password

    # The user wants to get all their active issues
    result = runner.invoke(jira)
    assert result.exit_code == 0

