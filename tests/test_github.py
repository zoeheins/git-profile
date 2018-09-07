from unittest import mock, TestCase

import requests

from git_profile.github import Github
from git_profile.github_user import GithubUser
from tests.test_utils import mock_resp


class TestGithub(TestCase):

    def setUp(self):
        self.api = Github(base_url='foo.com')

    def test_base_url(self):
        self.assertEqual(self.api.base_url, 'foo.com')

    @mock.patch('git_profile.github.requests.get')
    def test_get_requests_api_with_full_url(self, mock_get):
        mock_get.return_value = mock_resp({})

        self.api.get('/fake_path')
        mock_get.assert_called_with(
            'foo.com/fake_path',
            headers=mock.ANY,
            params=mock.ANY,
        )

    @mock.patch('git_profile.github.requests.get')
    def test_get_bad_api_response_raises_exception(self, mock_get):
        mock_get.return_value = mock_resp({}, status_code=500)
        with self.assertRaises(Exception):
            self.api.get('/blah')


    @mock.patch('git_profile.github.requests.get')
    def test_get_returns_api_data(self, mock_get):
        mock_get.return_value = mock_resp({'a': 'b'})
        data = self.api.get('/blah')
        self.assertEqual(data, {'a': 'b'})

    @mock.patch('git_profile.github.requests.get')
    def test_get_calls_next_url_when_paginated_api_resp(self, mock_get):
        first_page = mock.MagicMock()
        first_page.status_code = 200
        first_page.links = {'next': {'url': 'some_url'}}

        second_page = mock.MagicMock()
        second_page.status_code = 200
        second_page.json.return_value = ['item1']
        second_page.links = {}

        mock_get.side_effect = [first_page, second_page]

        self.assertEqual(
            self.api.get('/blah'),
            ['item1']
        )

    def test_user(self):
        user = self.api.user('fake_name')
        self.assertIsInstance(user, GithubUser)
