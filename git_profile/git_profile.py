from .github import Github
from .bitbucket import Bitbucket


class GitProfile():
    """Represents the combined profile for a bitbucket and github user"""

    def __init__(self, github_username, bitbucket_username):
        self.github = Github().user(github_username)
        self.bitbucket = Bitbucket().user(bitbucket_username)

    def merged(self):
        """Returns merged profile (dict)"""
        return {
            'public_repos': self._combine_repos(),
            'followers': self._combine('total_followers'),
            'stars_given': self._combine('total_stars_given'),
            'open_issues': self._combine('total_open_issues'),
            'commits': self._combine('total_commits'),
            'languages_used': self._combine_lists('languages_used'),
            'account_size': self._combine('account_size'),
            'repo_topics': self._combine_lists('repo_topics')
        }

    def _combine(self, attribute):
        """Returns sum (int) of github and bitbucket data"""
        total = (
            getattr(self.bitbucket, attribute, 0)() +
            getattr(self.github, attribute, 0)()
        )
        return total

    def _combine_lists(self, attribute):
        """Returns combined list of github and bitbucket data"""
        combined = (
            getattr(self.bitbucket, attribute, [])() +
            getattr(self.github, attribute, [])()
        )
        return list(set(combined))

    def _combine_repos(self):
        """Returns combined github and bitbucket repo totals (dict)"""
        bb = self.bitbucket.total_repos()
        gh = self.github.total_repos()
        keys = ['total', 'originals', 'forks']
        final = {}
        for key in keys:
            final[key] = bb[key] + gh[key]
        return final
