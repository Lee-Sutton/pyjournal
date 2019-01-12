from github import Github


class GithubConnection:
    """Connects to gihub api"""

    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._github = Github(username, password)

    def get_prs_awaiting_review(self):
        return self._github.search_issues(
            f'is:open is:pr review-requested:{self._username}')
