import pytest
from pyjournal.db.models import Task


def test_task_insert(db):
    """it should insert into the database and provide sensible defaults"""
    task = Task.create(name='dummy task', is_done=False)
    assert task.name == 'dummy task'
    assert task.created_at is not None
    assert task.is_done == False

