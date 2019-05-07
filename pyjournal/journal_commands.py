import os
import datetime
from pyjournal.db.models import Config
from pyjournal.utils import makedirs_touch
from pyjournal.editor import open_editor
from pyjournal.db import models
import click


@click.command()
@click.option('--path', default='~/Journal/', help='path to journal directory')
@click.option('--editor', default='vim', help='editor to open your journal')
def init(path, editor):
    """Initializes journal directory if it does not exist"""
    journal_path = os.path.abspath(os.path.expanduser(path))

    # FIXME prompt the user if it's already there
    models.Config.create(journal_dir=path, editor=editor)
    click.echo(f'Journal initialized at {journal_path}')

    if not os.path.exists(journal_path):
        os.makedirs(journal_path)


@click.command(name='open')
def open_journal():
    """Opens the journal"""
    config = Config.get()
    os.chdir(config.journal_dir)
    open_editor(config.journal_dir)


@click.command()
def today():
    """
    Opens the journal entry for today. A new document
    is created if it does not already exist
    """
    config = Config.get()
    today = datetime.datetime.today()
    journal_file = os.path.join(config.journal_dir,
                                f'{today.year}/{today.month}/{today.day}.md')

    makedirs_touch(journal_file)
    os.chdir(config.journal_dir)
    open_editor(journal_file)


@click.command()
@click.argument('topic_title')
def topic(topic_title):
    """Creates a new document for the input topic"""
    config = Config.get()

    filename = topic_title.replace(' ', '-')
    journal_file = os.path.join(config.journal_dir,
                                f'topics/{filename}.md')

    makedirs_touch(journal_file)
    os.chdir(config.journal_dir)
    open_editor(journal_file)
