#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyjournal` package."""

import os
from os import path
from unittest.mock import patch

import pytest
from freezegun import freeze_time
from tinydb import where

from pyjournal.journal_commands import init, today, tasks, topic, open_journal
from pyjournal.utils import makedirs_touch


@pytest.fixture()
def initialized_database(runner, journal_test_dir, test_db):
    """Returns an initialized instance of the database"""
    runner.invoke(init, args=['--path', journal_test_dir])
    yield test_db


@freeze_time('Jan 1 2020')
def test_init(runner, journal_test_dir, test_db):
    # The user initializes the journal
    result = runner.invoke(init, args=['--path', journal_test_dir])
    assert result.exit_code == 0
    assert f'Journal initialized at {journal_test_dir}' in result.output

    config = test_db.get(where('journal_path') == journal_test_dir)
    assert config['journal_path'] == journal_test_dir

    # A directory is created for the journal notes
    assert path.exists(journal_test_dir)


@freeze_time('Jan 1 2020')
@patch('pyjournal.journal_commands.open_editor', autospec=True)
def test_today(open_editor, initialized_database, runner,
               journal_test_dir):
    # The user wants to create a journal entry for today
    # A directory is created for the current year and month
    result = runner.invoke(today)
    assert result.exit_code == 0
    journal_file = path.join(journal_test_dir, '2020/1/1.md')

    # The user is cd'ed into the Journal Directory and vim is opened
    # with the new file
    assert os.getcwd() == journal_test_dir

    open_editor.assert_called_with(journal_file)


@patch('pyjournal.journal_commands.open_editor', autospec=True)
def test_open(open_editor, initialized_database, runner, journal_test_dir):
    # The user wants to create a journal entry for today
    # A directory is created for the current year and month
    result = runner.invoke(open_journal)
    assert result.exit_code == 0

    # The user is cd'ed into the Journal Directory and vim is opened
    # with the new file
    assert os.getcwd() == journal_test_dir
    open_editor.assert_called_with(journal_test_dir)


@freeze_time('Jan 1 2020')
@patch('pyjournal.journal_commands.open_editor', autospec=True)
def test_topic(open_editor, runner, journal_test_dir, initialized_database):
    """The user wants to a new journal file for the input topic"""
    result = runner.invoke(topic, args=['dummy topic'])
    assert result.exit_code == 0

    journal_file = path.join(journal_test_dir, f'topics/dummy-topic.md')
    open_editor.assert_called_with(journal_file)


@freeze_time('Jan 1 2020')
def test_todo(runner, journal_test_dir, initialized_database):
    """The user wants to list all the tasks in their journal"""
    journal_file = path.join(journal_test_dir, '2020/1/1.md')
    makedirs_touch(journal_file)

    # The user opens the journal and add some tasks
    task = 'TODO finish this task!'
    with open(journal_file, '+w') as f:
        f.write(task)

    result = runner.invoke(tasks)
    assert result.exit_code == 0
    assert task in result.output
