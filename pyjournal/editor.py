"""Editor module
Utility functions for interacting with the user's editor
"""
import subprocess

DEFAULT_EDITOR = 'nvim'


def open_editor(filename):
    """Opens the input file with the users default editor"""
    subprocess.call([DEFAULT_EDITOR, filename])
