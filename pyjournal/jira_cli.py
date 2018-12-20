import click
from requests.exceptions import MissingSchema
from tinydb import Query

from pyjournal.database import initialize_database
from pyjournal.jira_connection import Jira


def format_issue(issue):
    """Formats the jira issue for easy display/reading
    :param issue - Input issue to format
    :return {str} - Formatted string containing the issue number,
    name, type and status
    """
    return f'[${issue}] {issue.fields.summary}'


@click.command()
@click.option('--init', is_flag=True, help='initializes your jira connection')
def jira(init):
    """Lists jira tasks assigned to the user"""
    db = initialize_database()

    if init:
        url = click.prompt('Please enter your jira url')
        email = click.prompt('Please enter your email')
        password = click.prompt('Password', hide_input=True)

        try:
            Jira(url, email, password)
            db.insert({'jira': {
                'url': url,
                'email': email,
                'password': password,
            }})

        except MissingSchema:
            click.echo('Invalid Jira configuration check your url')

    else:
        config = db.get(Query().jira.exists())
        jira_config = config['jira']
        jira_connection = Jira(**jira_config)

        active_issues = jira_connection.active_issues()
        for issue in active_issues:
            click.echo(format_issue(issue))
