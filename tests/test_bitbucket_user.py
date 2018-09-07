from unittest import TestCase, mock

from git_profile.bitbucket_user import BitbucketUser


class TestBitbucketUser(TestCase):

    def setUp(self):
        self.api = mock.MagicMock()
        self.user = BitbucketUser(self.api, 'bb_name')

    def test_username(self):
        self.assertEqual(self.user.username, 'bb_name')

    def test_followers(self):
        self.api.get.return_value = ['some followers']
        self.assertEqual(self.user.total_followers(), 1)

    def test_total_repos(self):
        self.api.get.return_value = [{'a': 'repo'}, {'parent': 'foo'}]
        expected = {
            'total': 2,
            'originals': 1,
            'forks': 1
        }
        self.assertEqual(self.user.total_repos(), expected)

    def test_languages_used(self):
        self.api.get.return_value = [{'language': 'python'}]
        self.assertEqual(self.user.languages_used(), ['python'])

    def test_account_size(self):
        self.api.get.return_value = [{'size': 1}, {'size': 2}]
        self.assertEqual(self.user.account_size(), 3)

    def test_total_commits(self):
        repos_resp = [{'slug': 'foo'}]
        commits_resp = ['a commit']
        self.api.get.side_effect = [repos_resp, commits_resp]
        self.assertEqual(self.user.total_commits(), 1)
