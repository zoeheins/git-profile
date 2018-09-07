class GithubUser:
    """Represents a Github User"""

    def __init__(self, api, username):
        """
        api (git_profile.github.Github): instance of Github API wrapper
        username (str): github username
        """
        self.api = api
        self.username = username
        self._repos = []

    def total_followers(self):
        """Returns user's total followers (int) """
        url = f'/users/{self.username}'
        return self.api.get(url)['followers']

    def total_repos(self):
        """Returns user's total repos (dict), separated by:
           total, originals, forks
        """
        originals = []
        forks = []
        repos = self.repos()
        for repo in repos:
            if repo.get('parent'):
                forks.append(repo)
            else:
                originals.append(repo)
        return {
            'total': len(repos),
            'originals': len(originals),
            'forks': len(forks),
        }

    def repos(self):
        """Returns list of user's repos"""
        if not self._repos:
            self._repos = self.api.get(f'/users/{self.username}/repos')
        return self._repos

    def _stars_given(self):
        """Returns list of repos being starred by user"""
        url = f'/users/{self.username}/starred'
        return self.api.get(url)

    def total_stars_given(self):
        """Returns total repos starred by user (int)"""
        return len(self._stars_given())

    def languages_used(self):
        """Returns list of languages used throughout user's repos"""
        languages = []

        names = [repo['name'] for repo in self.repos()]
        for name in names:
            language = self.api.get(f'/repos/{self.username}/{name}/languages')
            languages.extend(language.keys())
        return list(set(languages))

    def total_open_issues(self):
        """Returns total open issues for user's repos (int)"""
        return len(self._open_issues())

    def _open_issues(self):
        """Returns list of open issues for user's repos"""
        issues = []
        for repo in self.repos():
            name = repo['name']
            resp = self.api.get(
                f'/repos/{self.username}/{name}/issues',
                params={'state': 'open'}
            )
            issues.extend(resp)
        return issues

    def account_size(self):
        """Returns size (int) of user's account"""
        sizes = [repo['size'] for repo in self.repos()]
        return sum(sizes)

    def repo_topics(self):
        """Returns list of topics labeled in user's repo"""
        headers = {'Accept': 'application/vnd.github.mercy-preview+json'}
        topics = []
        for repo in self.repos():
            name = repo['name']
            resp = self.api.get(
                f'/repos/{self.username}/{name}/topics',
                headers=headers
            )
            topics.extend(resp['names'])
        return sorted(list(set(topics)))

    def total_commits(self):
        return 0
