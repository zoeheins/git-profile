class BitbucketUser:
    """Represents a Bitbucker user or team"""

    def __init__(self, api, username):
        """
        api (git_profile.bitbucket.Bitbucket): instance of Bitbucket API wrapper
        username (str): bitbucket username
        """
        self.api = api
        self.username = username
        self._repos = []

    def repos(self):
        """Returns list of user's repositories"""
        if not self._repos:
            self._repos = self.api.get(f'/repositories/{self.username}')
        return self._repos

    def _followers(self):
        """Returns list of usrs' followers"""
        try:
            return self.api.get(f'/users/{self.username}/followers')
        except:
            return self.api.get(f'/teams/{self.username}/followers')

    def total_followers(self):
        """Returns usrer's total followers (int)"""
        return len(self._followers())

    def total_repos(self):
        """Returns user's total repos (dict), separated by:
           total, originals, forks
        """
        originals = []
        forks = []
        repos = self.repos()
        for repo in repos:
            if repo.get('parent'):
                forks.extend(repo)
            else:
                originals.extend(repo)
        return {
            'total': len(repos),
            'originals': len(originals),
            'forks': len(forks),
        }

    def total_commits(self):
        """Returns user's total commits (int)"""
        return len(self._commits())

    def _commits(self):
        """Returns list of user's commits"""
        commits = []
        for repo in self.repos():
            slug = repo['slug']
            repo_commits = self.api.get(f'/repositories/{self.username}/{slug}/commits')
            commits.extend(repo_commits)
        return commits

    def account_size(self):
        """Returns size (int) of user's account"""
        sizes = [repo['size'] for repo in self.repos()]
        return sum(sizes)

    def languages_used(self):
        """Returns list of languages used throughout user's repos"""
        languages = []
        for repo in self.repos():
            if repo['language']:
                languages.append(repo['language'])
        return list(set(languages))

    def total_open_issues(self):
        """Returns total open issues for user's repos (int)"""
        return len(self._open_issues())

    def _open_issues(self):
        """Returns list of open issues for user's repos"""
        issues = []
        for repo in self.repos():
            try:
                slug = repo['slug']
                resp = self.api.get(
                    f'/repositories/{self.username}/{slug}/issues',
                    params={'status': 'open'}
                )
                issues.extend(resp)
            except:
                pass
        return issues

    def total_stars_given(self):
        return 0

    def repo_topics(self):
        return []
