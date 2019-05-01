"""model test suite"""
import pytest
from pyjournal.db.models import Task, initialize_db


def test_task_insert():
    """it should insert into the database and provide sensible defaults"""
    initialize_db()
    task = Task.create(name="dummy task", is_done=False)
    assert task.name == "dummy task"
    assert task.created_at is not None
    assert task.is_done is False
    assert task.is_archived is False
