# -*- coding: utf-8 -*-

"""Test suite for the database module"""
import os
import pytest
from pyjournal.utils import makedirs_touch


@pytest.fixture
def tmp_filepath(tmpdir):
    yield os.path.join(tmpdir, '.config/pyjournal/config.json')


def test_directory_created(tmp_filepath):
    """
    it should create a directory for the database if it does not already exist
    """
    makedirs_touch(tmp_filepath)
    assert os.path.exists(tmp_filepath)


def test_does_not_destroy_file(tmpdir):
    """It should use the supplied database file if it exists"""
    created_file = tmpdir.join('config.json')
    created_file.write('content')

    makedirs_touch(created_file)

    assert 'content' in created_file.read()
