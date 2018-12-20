"""Jira connection test suite"""
from pyjournal.jira_cli import jira
from unittest.mock import patch, MagicMock
from tinydb import Query
import pytest
from requests.exceptions import MissingSchema

URL = 'dummy_url'
EMAIL = 'lee@e.com'
PASSWORD = '123456'


@pytest.fixture()
def jira_populated_db(test_db):
    test_db.insert({'jira': {
        'url': URL,
        'email': EMAIL,
        'password': PASSWORD,
    }})


@pytest.fixture()
def mock_issue():
    issue = MagicMock()
    issue.__str__.return_value = 'test issue'
    return issue


@patch('pyjournal.jira_cli.Jira')
def test_jira_init(mock_jira, runner, test_db):
    """It should allow the user to initialize their jira settings"""
    result = runner.invoke(jira, args=['--init'], input=f'{URL}\n{EMAIL}\n{PASSWORD}\n')
    assert result.exit_code == 0

    mock_jira.assert_called_with(URL, EMAIL, PASSWORD)

    # The data should be stored in the database
    config = test_db.get(Query().jira.exists())
    jira_config = config['jira']
    assert jira_config is not None
    assert jira_config['url'] == URL
    assert jira_config['email'] == EMAIL
    assert jira_config['password'] == PASSWORD


@patch('pyjournal.jira_cli.Jira')
def test_invalid_jira_connection(mock_jira, runner):
    """
    It should inform the user if the jira url is invalid
    """
    mock_jira.side_effect = MissingSchema('Invalid URL')
    result = runner.invoke(jira, args=['--init'], input=f'{URL}\n{EMAIL}\n{PASSWORD}\n')
    mock_jira.assert_called()
    assert 'Invalid Jira' in result.output


@patch('pyjournal.jira_cli.Jira')
def test_jira_issues(mock_jira, runner, jira_populated_db, mock_issue):
    """
    Given: The user has already initialized their jira connection
    Expect: The user should be able to fetch all their jira issues
    """
    mock_jira().active_issues.return_value = [mock_issue]
    result = runner.invoke(jira)
    assert result.exit_code == 0
    mock_jira.assert_called_with(url=URL, email=EMAIL, password=PASSWORD)
    assert str(mock_issue) in result.output
