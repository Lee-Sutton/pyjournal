import os
import subprocess

import click
from tinydb import Query

from pyjournal.database import initialize_database
from pyjournal.db.models import Task


@click.command()
def tasks():
    """Lists all tasks in the journal"""
    db = initialize_database()
    config = db.get(Query().journal_path.exists())
    os.chdir(config['journal_path'])
    tasks = subprocess.check_output(['grep', '-ri', 'TODO', '.'])
    click.echo(tasks)


@click.command()
@click.argument('task')
def add_task(task):
    pass
