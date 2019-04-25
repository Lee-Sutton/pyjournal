import peewee
import datetime

DATABASE = peewee.SqliteDatabase("tasks.db")


class Task(peewee.Model):
    name = peewee.CharField()
    is_done = peewee.DateTimeField(default=datetime.datetime.now())
    created_at = peewee.BitField(default=False)
    # TODO add this
    # created_at =
    class Meta:
        database = DATABASE

def initialize_db():
    DATABASE.connect()
    DATABASE.create_tables([Task], safe = True)
    DATABASE.close()
