"""model test suite"""
from pyjournal.db.models import Task, Config


def test_task_insert(test_db):
    """it should insert into the database and provide sensible defaults"""
    # initialize_db()
    task = Task.create(name="dummy task", is_done=False)
    assert task.name == "dummy task"
    assert task.created_at is not None
    assert task.is_done is False
    assert task.is_archived is False


def test_config_model():
    """It should insert into the database"""
    config = Config.create(journal_dir='dummy dir', editor='vim')
    assert config is not None
