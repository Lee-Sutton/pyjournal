"""Database models"""
import datetime
import os
import peewee

DEFAULT_DATABASE_DIRECTORY = os.path.join(os.path.dirname(__file__),
                                          'db.sqlite3')

DATABASE = peewee.SqliteDatabase(DEFAULT_DATABASE_DIRECTORY)


class Task(peewee.Model):
    """Tasks model for storing todo items in the db"""

    name = peewee.CharField()
    is_done = peewee.DateTimeField(default=datetime.datetime.now())
    created_at = peewee.BitField(default=False)
    is_archived = peewee.BitField(default=False)

    class Meta:
        database = DATABASE


class Config(peewee.Model):
    """Model for storing user configuration"""
    journal_dir = peewee.CharField()
    editor = peewee.CharField()

    class Meta:
        database = DATABASE


TABLES = [Task, Config]


def initialize_db():
    """initializes the database and creates the required tables"""
    try:
        DATABASE.connect()
        DATABASE.create_tables(TABLES, safe=True)
        DATABASE.close()
    except peewee.OperationalError:
        pass


initialize_db()
