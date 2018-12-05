import click
from tinydb import Query
from pyjournal.database import initialize_database


@click.command()
@click.option('--init', is_flag=True, help='initializes your jira connection')
def jira(init):
    """Lists jira tasks assigned to the user"""
    db = initialize_database()
    url = click.prompt('Please enter your jira url')
    email = click.prompt('Please enter your email')
    password = click.prompt('Password', hide_input=True)

    if init:
        test_jira_connection(url, email, password)
        db.insert({'jira': {
            'url': url,
            'email': email,
            'password': password,
        }})
    else:
        config = db.get(Query().jira.exists())
        jira_config = config['jira']
        issues = get_active_issues(JIRA(
            jira_config['url'],
            auth=(jira_config['email'], jira_config['password'])
        ))
        for issue in issues:
            print()
