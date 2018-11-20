#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyjournal` package."""

import pytest

from os import path

from click.testing import CliRunner

from pyjournal import pyjournal
from pyjournal import cli


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture
def journal_test_dir(tmpdir):
    test_journal_path = path.join(tmpdir, 'Journal')
    yield test_journal_path

def test_init(runner, journal_test_dir):
    """Test the init journal command"""
    result = runner.invoke(cli.init, args=['--path', journal_test_dir])
    assert result.exit_code == 0
    assert f'Journal initialized at {journal_test_dir}' in result.output
    assert path.exists(journal_test_dir)
    assert path.exists(path.join(journal_test_dir, '2018/11'))
