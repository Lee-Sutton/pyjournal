import click
from tinydb import Query
from pyjournal.database import initialize_database
from pyjournal.jira_connection import Jira


@click.command()
@click.option('--init', is_flag=True, help='initializes your jira connection')
def jira(init):
    """Lists jira tasks assigned to the user"""
    db = initialize_database()

    if init:
        url = click.prompt('Please enter your jira url')
        email = click.prompt('Please enter your email')
        password = click.prompt('Password', hide_input=True)

        Jira(url, email, password)

        db.insert({'jira': {
            'url': url,
            'email': email,
            'password': password,
        }})
    else:
        config = db.get(Query().jira.exists())
        jira_config = config['jira']
        jira_connection = Jira(**jira_config)
        for issue in jira_connection.active_issues():
            print(issue)
