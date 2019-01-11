#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyjournal` package."""

from os import path
from unittest.mock import patch

import pytest
from freezegun import freeze_time
from tinydb import where

from pyjournal.journal_commands import init, today, tasks


@pytest.mark.func
@freeze_time('Jan 1 2020')
@patch('os.chdir')
@patch('subprocess.call')
def test_cli(subprocess_mock, chdir_mock, runner, journal_test_dir, test_db):
    """Functional test suite for the cli"""

    # The user initializes the journal
    result = runner.invoke(init, args=['--path', journal_test_dir])
    assert result.exit_code == 0
    assert f'Journal initialized at {journal_test_dir}' in result.output

    config = test_db.get(where('journal_path') == journal_test_dir)
    assert config['journal_path'] == journal_test_dir

    # A directory is created for the journal notes
    assert path.exists(journal_test_dir)

    # The user wants to create a journal entry for today
    # A directory is created for the current year and month
    result = runner.invoke(today)
    assert result.exit_code == 0
    journal_file = path.join(journal_test_dir, '2020/1/1.md')
    assert path.exists(journal_file)

    # The user is cd'ed into the Journal Directory and vim is opened
    # with the new file
    chdir_mock.assert_called_with(config['journal_path'])
    subprocess_mock.assert_called_with(['nvim', journal_file])

    # The user opens the journal and add some tasks
    task = 'TODO finish this task!'
    with open(journal_file, 'w') as f:
        f.write(task)

    result = runner.invoke(tasks)
    assert result.exit_code == 0
    chdir_mock.assert_called_with(config['journal_path'])
    subprocess_mock.assert_called_with(['grep', '-ri', 'TODO', '.'])