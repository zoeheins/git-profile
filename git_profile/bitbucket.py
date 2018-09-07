import requests

from .bitbucket_user import BitbucketUser

BB_BASE_URL = 'https://api.bitbucket.org/2.0'


class BitbucketApiError(Exception):
    pass


class Bitbucket:
    """Wrapper for Bitbucket API"""

    def __init__(self, base_url=BB_BASE_URL):
        self.base_url = base_url

    def user(self, username):
        """Returns an instance of BitbuckeUser"""
        return BitbucketUser(self, username)

    def get(self, path, params={}):
        """Calls Bitbucket API and returns result (dict or list)"""

        url = f'{self.base_url}{path}'
        resp = requests.get(url, params=params)

        if resp.status_code == 500:
            raise BitbucketApiError
        elif resp.status_code != 200:
            raise Exception
        if resp.json().get('next'):
            return self._get_depaginated(url)
        else:
            return resp.json()['values']

    def _get_depaginated(self, next_url):
        """Iterates through pages and return collected results (dict or list)"""
        items = []
        while next_url:
            resp = requests.get(next_url)
            if resp.status_code == 200:
                items.extend(resp.json()['values'])
                next_url = resp.json().get('next')
            else:
                break
        return items
