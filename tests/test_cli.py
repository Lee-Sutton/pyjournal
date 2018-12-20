from pyjournal.cli import cli


def test_cli(runner):
    result = runner.invoke(cli, args=['--help'])
    assert result.exit_code == 0
    assert 'init' in result.output
    assert 'today' in result.output
    assert 'tasks' in result.output
    assert 'jira' in result.output
