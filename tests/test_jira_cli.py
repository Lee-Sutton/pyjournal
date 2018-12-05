"""Jira connection test suite"""
from pyjournal.jira_cli import jira
from unittest.mock import patch
from tinydb import Query
import pytest

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
def test_jira_issues(mock_jira, runner, jira_populated_db):
    """
    Given: The user has already initialized their jira connection
    Expect: The user should be able to fetch all their jira issues
    """
    mock_jira().active_issues.return_value = ['test issue']
    result = runner.invoke(jira)
    assert result.exit_code == 0
    mock_jira.assert_called_with(url=URL, email=EMAIL, password=PASSWORD)
    assert 'test issue' in result.output
