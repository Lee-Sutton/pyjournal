import os
import subprocess

import click

from pyjournal.models import Task, Config


@click.command()
def tasks():
    """Lists all tasks in the journal"""
    config = Config.get()
    os.chdir(config.journal_dir)
    tasks = subprocess.check_output(['grep', '-ri', 'TODO', '.'])
    click.echo(tasks)


@click.command(name='t')
@click.argument('task')
def add_task(task):
    """Add a new todo"""
    Task.create(name=task)


@click.command()
def todos():
    """List all current todos"""
    content = [f'- [ ] {task.name}' for task in Task.select()]
    result = click.edit('\n'.join(content))
    click.echo(result)
