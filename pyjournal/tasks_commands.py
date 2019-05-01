import os
import subprocess

import click
from tinydb import Query

from pyjournal.database import initialize_database
from pyjournal.db.models import Task, initialize_db


@click.command()
def tasks():
    """Lists all tasks in the journal"""
    db = initialize_database()
    config = db.get(Query().journal_path.exists())
    os.chdir(config['journal_path'])
    tasks = subprocess.check_output(['grep', '-ri', 'TODO', '.'])
    click.echo(tasks)


@click.command(name='t')
@click.argument('task')
def add_task(task):
    """Add a new todo"""
    initialize_db()
    Task.create(name=task)


@click.command()
def todos():
    """List all current todos"""
    initialize_db()
    for task in Task.select():
        click.echo(task.name)
