# -*- coding: utf-8 -*-

"""Console script for pyjournal."""
import click
import os
import datetime


@click.group()
def cli():
    pass


@click.command()
@click.option('--path', default='~/Journal/', help='path to journal directory')
def init(path):
    """Initializes journal directory if it does not exist"""
    journal_path = os.path.abspath(path)
    click.echo(f'Journal initialized at {journal_path}')
    os.makedirs(journal_path)


@click.command()
def today():
    """
    Opens the journal entry for today. A new document
    is created if it does not already exist
    """
    print('this was invoked')
    today = datetime.datetime.today()
    os.makedirs(os.path.join(journal_path, f'{today.year}/{today.month}'))


cli.add_command(init)

if __name__ == "__main__":
    cli()
