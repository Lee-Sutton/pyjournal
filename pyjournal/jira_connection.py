import click
from jira import JIRA

from pyjournal.database import initialize_database


def test_jira_connection(url, email, password):
    JIRA(url, auth=(email, password))


@click.command()
@click.option('--init', is_flag=True, help='initializes your jira connection')
def jira(init):
    """Lists jira tasks assigned to the user"""
    url = click.prompt('Please enter your jira url')
    email = click.prompt('Please enter your email')
    password = click.prompt('Password', hide_input=True)

    if init:
        test_jira_connection(url, email, password)
        db = initialize_database()
        db.insert({'jira': {
            'url': url,
            'email': email,
            'password': password,
        }})


def main():
    jira_connection = JIRA('https://keelanetworksforchange.atlassian.net/',
                           auth=('lee.sutton@networksforchange.org', 'LucyDog2009'))

    # for project in jira_connection.projects():
    #     print(project)

    # project = jira_connection.project('KEEL')
    # print(dir(project))
    # print(project.id)

    # print(dir(jira_connection.sprints(board_id=1)[0]))
    for sprint in jira_connection.sprints(board_id=1):
        print(sprint.state)
        if sprint.state == 'ACTIVE':
            issues = jira_connection.search_issues(f'sprint={sprint.id} AND assignee = currentUser()')
            for issue in issues:
                print(issue)
                print(issue.fields.summary)
                print(issue.fields.status)

    # sprint = jira_connection.sprint(1)
    # print(dir(sprint))

    # print(jira_connection.search_issues('sprint=1'))

    # assigned_issues = jira_connection.search_issues('assignee=currentUser()')

    # my top 5 issues due by the end of the week, ordered by priority
    # oh_crap = jira_connection.search_issues('assignee = currentUser() and sprint=Nov 23 - Dec 7')

    # # Summaries of my last 3 reported issues
    # for issue in jira.search_issues('reporter = currentUser() order by created desc', maxResults=3):
    #     print('{}: {}'.format(issue.key, issue.fields.summary))

    # for issue in assigned_issues:
    #     print(issue)


if __name__ == '__main__':
    main()
