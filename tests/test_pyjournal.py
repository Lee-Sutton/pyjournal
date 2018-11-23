#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyjournal` package."""

import os
from os import path
from unittest.mock import patch

import pytest
from click.testing import CliRunner
from freezegun import freeze_time
from tinydb import where

from pyjournal import cli
from pyjournal.database import initialize_database


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture
def journal_test_dir(tmpdir):
    test_journal_path = path.join(tmpdir, 'Journal')
    yield test_journal_path


@pytest.fixture()
def test_db(tmpdir):
    """creates a temporary database for testing"""
    os.environ['DB_PATH'] = str(tmpdir.join('config.json'))
    yield initialize_database()
    os.environ.pop('DB_PATH')


@pytest.mark.func
@freeze_time('Jan 1 2020')
@patch('subprocess.call')
def test_cli(subprocess_mock, runner, journal_test_dir, test_db):
    """Functional test suite for the cli"""

    # The user initializes the journal
    result = runner.invoke(cli.init, args=['--path', journal_test_dir])
    assert result.exit_code == 0
    assert f'Journal initialized at {journal_test_dir}' in result.output

    config = test_db.get(where('journal_path') == journal_test_dir)
    assert config['journal_path'] == journal_test_dir
    # A directory is created for the journal notes
    assert path.exists(journal_test_dir)

    # The user wants to create a journal entry for today
    # A directory is created for the current year and month
    result = runner.invoke(cli.today)
    assert result.exit_code == 0
    journal_file = path.join(journal_test_dir, '2020/1/1.md')
    assert path.exists(journal_file)

    # The user is cd'ed into the Journal Directory and vim is opened
    # with the new file
    subprocess_mock.assert_called_with(['cd', config['journal_path'], '&&', 'vim', journal_file])


