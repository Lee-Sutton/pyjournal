#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyjournal` package."""

from os import path

import pytest
from click.testing import CliRunner
from freezegun import freeze_time

from pyjournal import cli


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture
def journal_test_dir(tmpdir):
    test_journal_path = path.join(tmpdir, 'Journal')
    yield test_journal_path


@pytest.mark.func
@freeze_time('Jan 1 2020')
def test_cli(runner, journal_test_dir):
    """Functional test suite for the cli"""

    # The user initializes the journal
    result = runner.invoke(cli.init, args=['--path', journal_test_dir])
    assert result.exit_code == 0
    assert f'Journal initialized at {journal_test_dir}' in result.output

    # A directory is created for the journal notes
    assert path.exists(journal_test_dir)

    # The user wants to create a journal entry for today
    # A directory is created for the current year and month
    result = runner.invoke(cli.today)
    assert result.exit_code == 0
    assert path.exists(path.join(journal_test_dir, '2020/1'))

