import subprocess
import os
import datetime
from pyjournal.database import initialize_database
from pyjournal.utils import makedirs_touch
from pyjournal.editor import open_editor
from tinydb import Query
import click


@click.command()
@click.option('--path', default='~/Journal/', help='path to journal directory')
def init(path):
    """Initializes journal directory if it does not exist"""
    db = initialize_database()
    journal_path = os.path.abspath(os.path.expanduser(path))
    click.echo(f'Journal initialized at {journal_path}')
    db.insert({'journal_path': journal_path})
    # FIXME prompt the user if it's already there

    if not os.path.exists(journal_path):
        os.makedirs(journal_path)


@click.command(name='open')
def open_journal():
    """Opens the journal"""
    db = initialize_database()
    config = db.get(Query().journal_path.exists())
    os.chdir(config['journal_path'])
    open_editor(config['journal_path'])


@click.command()
def today():
    """
    Opens the journal entry for today. A new document
    is created if it does not already exist
    """
    db = initialize_database()
    config = db.get(Query().journal_path.exists())
    today = datetime.datetime.today()
    journal_file = os.path.join(config['journal_path'],
                                f'{today.year}/{today.month}/{today.day}.md')

    makedirs_touch(journal_file)
    os.chdir(config['journal_path'])
    open_editor(journal_file)


@click.command()
def tasks():
    """Lists all tasks in the journal"""
    db = initialize_database()
    config = db.get(Query().journal_path.exists())
    os.chdir(config['journal_path'])
    tasks = subprocess.check_output(['grep', '-ri', 'TODO', '.'])
    click.echo(tasks)


@click.command()
@click.argument('topic_title')
def topic(topic_title):
    """Creates a new document for the input topic"""
    db = initialize_database()
    config = db.get(Query().journal_path.exists())
    today = datetime.datetime.today()

    filename = topic_title.replace(' ', '-')
    journal_file = os.path.join(config['journal_path'],
                                f'topics/{filename}.md')

    makedirs_touch(journal_file)
    os.chdir(config['journal_path'])
    open_editor(journal_file)
