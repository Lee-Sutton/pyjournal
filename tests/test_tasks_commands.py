from os import path
from freezegun import freeze_time
from unittest.mock import patch
from pyjournal.utils import makedirs_touch
from pyjournal.tasks_commands import tasks, add_task, todos
from pyjournal.models import Task


@freeze_time('Jan 1 2020')
def test_todo(runner, journal_test_dir, initialized_journal):
    """The user wants to list all the tasks in their journal"""
    journal_file = path.join(journal_test_dir, '2020/1/1.md')
    makedirs_touch(journal_file)

    # The user opens the journal and add some tasks
    task = 'TODO finish this task!'
    with open(journal_file, '+w') as f:
        f.write(task)

    result = runner.invoke(tasks)
    assert result.exit_code == 0
    assert task in result.output


def test_add_task(test_db, runner):
    """it should add a task to the db"""
    task = 'dummy task here'
    result = runner.invoke(add_task, args=[task])
    assert result.exit_code == 0
    saved_task = Task.select().where(Task.name == task)
    assert len(saved_task)


@patch('pyjournal.tasks_commands.click.edit')
def test_todos(mock_edit, test_db, runner):
    """it should list tasks in the database"""
    task = 'dummy task here'
    Task.create(name=task)
    result = runner.invoke(todos)
    assert result.exit_code == 0
    mock_edit.assert_called_with(f'- [ ] {task}')
