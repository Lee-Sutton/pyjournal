from github import Github


class GithubConnection:
    """Connects to gihub api"""
    def __init__(self, username, password):
        self._github = Github(username, password)

    def get_issues(self):
        pass
