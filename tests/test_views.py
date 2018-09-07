from unittest import mock, TestCase

from flask import Flask, request

from git_profile import app
from git_profile.github import GithubApiError
from git_profile.bitbucket import BitbucketApiError


class TestViews(TestCase):

    def test_returns_error_when_missing_params(self):
        with app.test_client() as c:
            resp = c.get('/profiles')
            expected = {
                'status': 'error',
                'message': 'Please provide a Github and Bitbucket username'
            }
            self.assertEqual(resp.json, expected)
            self.assertEqual(resp.status_code, 400)

    @mock.patch('git_profile.views.GitProfile')
    def test_returns_user_profile(self, mock_profile):
        with app.test_client() as c:
            profile_instance = mock_profile.return_value
            profile_instance.merged.return_value = {'some': 'thing'}
            resp = c.get('/profiles?gh=foo&bb=bar')
            expected = {
                'status': 'ok',
                'profile': {'some': 'thing'},
            }
            self.assertEqual(resp.json, expected)
            self.assertEqual(resp.status_code, 200)

    @mock.patch('git_profile.views.GitProfile')
    def test_interal_error(self, mock_profile):
        with app.test_client() as c:
            profile_instance = mock_profile.return_value
            profile_instance.merged.side_effect = Exception
            resp = c.get('/profiles?gh=foo&bb=bar')
            expected = {
                'status': 'error',
                'message': 'An internal error occured',
            }
            self.assertEqual(resp.json, expected)
            self.assertEqual(resp.status_code, 500)

    @mock.patch('git_profile.views.GitProfile')
    def test_github_api_error(self, mock_profile):
        with app.test_client() as c:
            profile_instance = mock_profile.return_value
            profile_instance.merged.side_effect = GithubApiError
            resp = c.get('/profiles?gh=foo&bb=bar')
            expected = {
                'status': 'error',
                'message': 'Error occured trying to connect to Github API',
            }
            self.assertEqual(resp.json, expected)
            self.assertEqual(resp.status_code, 502)

    @mock.patch('git_profile.views.GitProfile')
    def test_bitbucket_apiinteral_error(self, mock_profile):
        with app.test_client() as c:
            profile_instance = mock_profile.return_value
            profile_instance.merged.side_effect = BitbucketApiError
            resp = c.get('/profiles?gh=foo&bb=bar')
            expected = {
                'status': 'error',
                'message': 'Error occured trying to connect to Bitbucket API',
            }
            self.assertEqual(resp.json, expected)
            self.assertEqual(resp.status_code, 502)
