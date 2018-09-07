import requests

from . import app
from .github_user import GithubUser

GH_BASE_URL = 'https://api.github.com'


class GithubApiError(Exception):
    pass


class Github:
    """Wrapper for Github API"""

    def __init__(self, base_url=GH_BASE_URL):
        self.base_url = base_url
        self.token = app.config.get('GITHUB_TOKEN')

    def user(self, username):
        """Returns instance of GithubUser"""
        return GithubUser(self, username)

    def get(self, path, params={}, headers={}):
        """Calls Github API and returns results (dict or list)"""

        if self.token:
            headers.update({'Authorization': f'token {self.token}'})

        # explicitly set api version
        headers.update({'Accept': 'application/vnd.github.v3+json'})

        url = f'{self.base_url}{path}'
        resp = requests.get(url, headers=headers, params=params)

        if resp.status_code == 500:
            raise GithubApiError
        elif resp.status_code != 200:
            raise Exception
        if resp.links:
            return self._get_depaginated(url)
        return resp.json()

    def _get_depaginated(self, url):
        """Iterates through pages and returns collected result (list)"""
        items = []
        while url:
            resp = requests.get(url)
            if resp.status_code == 200:
                items.extend(resp.json())
                url = resp.links.get('next', {}).get('url')
            else:
                break
        return items
