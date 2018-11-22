# -*- coding: utf-8 -*-

"""Database management and inititialization"""
import os


def makedirs_touch(path):
    """Creates the file and all parent directories in the supplied path"""
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    with open(path, 'a'):
        os.utime(path, None)

