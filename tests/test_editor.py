"""Editor test suite"""
from pyjournal.editor import open_editor
from unittest.mock import patch


@patch('pyjournal.editor.subprocess')
def test_open_editor(subprocess_mock):
    filename = 'test-file.txt'
    open_editor(filename)
    subprocess_mock.call.assert_called_with(['nvim', filename])
