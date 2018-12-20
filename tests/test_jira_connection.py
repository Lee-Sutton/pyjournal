from collections import namedtuple
from unittest.mock import patch
from pyjournal.jira_connection import Jira
import faker
from faker.providers import internet

fake = faker.Faker()
fake.add_provider(internet)


@patch('pyjournal.jira_connection.JIRA')
def test_jira(jira_api):
    url = fake.url()
    email = fake.email()
    password = 'password'

    Jira(url, email, password)

    jira_api.assert_called_with(url, auth=(email, password))


Sprint = namedtuple('Sprint', ['state', 'id'])


@patch('pyjournal.jira_connection.JIRA')
def test_active_issues(jira_api):
    url = fake.url()
    email = fake.email()
    password = 'password'

    jira_api().sprints.return_value = [Sprint('ACTIVE', 1), Sprint('INACTIVE', 2)]

    jira = Jira(url, email, password)
    board_id = 2
    issues = jira.active_issues(board_id)

    assert issues is not None
    jira_api().sprints.assert_called_with(board_id=board_id)
    jira_api().search_issues.assert_called()
