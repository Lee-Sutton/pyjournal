"""Database models"""
import datetime
import peewee

DATABASE = peewee.SqliteDatabase("tasks.db")


class Task(peewee.Model):
    """Tasks model for storing todo items in the db"""

    name = peewee.CharField()
    is_done = peewee.DateTimeField(default=datetime.datetime.now())
    created_at = peewee.BitField(default=False)

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
