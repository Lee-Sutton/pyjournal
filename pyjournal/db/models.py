"""Database models"""
import datetime
import os
import peewee

DEFAULT_DATABASE_DIRECTORY = os.path.join(os.path.dirname(__file__), "db.sqlite3")

DATABASE = peewee.SqliteDatabase(DEFAULT_DATABASE_DIRECTORY)


class Task(peewee.Model):
    """Tasks model for storing todo items in the db"""

    name = peewee.CharField()
    is_done = peewee.DateTimeField(default=datetime.datetime.now())
    created_at = peewee.BitField(default=False)
    is_archived = peewee.BitField(default=False)

    class Meta:
        database = DATABASE


TABLES = [Task]


def initialize_db():
    """initializes the database and creates the required tables"""
    DATABASE.connect()
    DATABASE.create_tables(TABLES, safe=True)
    DATABASE.close()


def drop_db():
    """clears the database and drops all tables"""
    DATABASE.drop_tables(TABLES, safe=True)
    DATABASE.close()
