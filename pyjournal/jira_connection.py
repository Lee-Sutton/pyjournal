from jira import JIRA

DEFAULT_BOARD = 1


class Jira:
    """Connects to the Jira API"""

    def __init__(self, url, email, password):
        self._jira = JIRA(url, auth=(email, password))

    def active_issues(self, board_id=DEFAULT_BOARD):
        """Searches for active issues on the input board"""
        for sprint in self._jira.sprints(board_id=board_id):
            if sprint.state == 'ACTIVE':
                return self._jira.search_issues(f'sprint={sprint.id} AND assignee = currentUser()')
