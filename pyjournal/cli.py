# -*- coding: utf-8 -*-

"""Console script for pyjournal."""

import click
from pyjournal.jira_commands import jira
from pyjournal.journal_commands import init, today, tasks


@click.group()
def cli():
    pass


cli.add_command(init)
cli.add_command(today)
cli.add_command(tasks)
cli.add_command(jira)

if __name__ == "__main__":
    cli()
