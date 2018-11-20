# -*- coding: utf-8 -*-

"""Console script for pyjournal."""
import sys
import click
import os


@click.group()
def cli():
    pass


@click.command()
@click.option('--path', default='~/Journal/', help='path to journal directory')
def init(path):
    """Initializes journal directory if it does not exist"""
    journal_path = os.path.abspath(path)
    click.echo(f'Journal initialized at {journal_path}')
    os.makedirs(os.path.join(journal_path, '2018/11'))

cli.add_command(init)

if __name__ == "__main__":
    cli()
