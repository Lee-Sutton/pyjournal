import os
import subprocess
import collections

import click

from pyjournal.models import Task, Config

CompletedItem = collections.namedtuple('CompletedItem',
                                       ['is_complete', 'description'])


def parse_markdown_checkboxes(content) -> [CompletedItem]:
    result = []
    for line in content.split('\n'):
        is_complete = line[4] != ' '
        content = line[6:]
        result.append(CompletedItem(is_complete, content))

    return result


def complete_tasks(completed_items: [CompletedItem]):
    for task in completed_items:
        Task.update(is_done=task.is_complete).where(
            Task.name == task.description).execute()


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
