import os
from pyjournal.utils import makedirs_touch
from tinydb import TinyDB

DEFAULT_DATABASE_DIRECTORY = os.path.join(os.path.dirname(__file__),
                                          '../config.json')


def initialize_database():
    path = os.getenv('DB_PATH', DEFAULT_DATABASE_DIRECTORY)
    makedirs_touch(path)
    return TinyDB(path)
