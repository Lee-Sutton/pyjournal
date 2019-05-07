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
    for task in Task.select():
        click.echo(f'{task.id}) {task.name}')
