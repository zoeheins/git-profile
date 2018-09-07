from unittest import TestCase, mock

from git_profile.github_user import GithubUser


class TestGithubUser(TestCase):

    def setUp(self):
        self.api = mock.MagicMock()
        self.user = GithubUser(self.api, 'fake_name')

    def test_api(self):
        self.assertEqual(self.user.api, self.api)

    def test_username(self):
        self.assertEqual(self.user.username, 'fake_name')

    def test_total_followers(self):
        self.api.get.return_value = {'followers': 10}
        self.assertEqual(self.user.total_followers(), 10)

    def test_total_repos(self):
        self.api.get.return_value = [{'a': 'repo'}, {'parent': 'forked'}]
        expected = {
            'total': 2,
            'originals': 1,
            'forks': 1
        }
        self.assertEqual(self.user.total_repos(), expected)

    def test_languages_used(self):
        repo_resp = [{'name': 'repo1', 'name': 'repo2'}]
        languages_resp = {'python': 1}
        self.api.get.side_effect = [repo_resp, languages_resp]
        self.assertEqual(self.user.languages_used(), ['python'])

    def test_account_size(self):
        self.api.get.return_value = [{'size': 1}, {'size': 2}]
        self.assertEqual(self.user.account_size(), 3)

    def test_repo_topics(self):
        repos = [{'name': 'a repo'}]
        topics = {'names': ['foo', 'bar', 'foo']}
        self.api.get.side_effect = [repos, topics]
        self.assertEqual(self.user.repo_topics(), ['bar', 'foo'])

