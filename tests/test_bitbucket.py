from unittest import mock, TestCase

from git_profile.bitbucket import Bitbucket
from git_profile.bitbucket_user import BitbucketUser
from tests.test_utils import mock_resp


class TestBitbucket(TestCase):

    def setUp(self):
        self.api = Bitbucket(base_url='bar.com')

    def test_base_url(self):
        self.assertEqual(self.api.base_url, 'bar.com')

    def test_user(self):
        user = self.api.user('fake_username')
        self.assertIsInstance(user, BitbucketUser)

    @mock.patch('git_profile.bitbucket.requests.get')
    def test_get_returns_api_data(self, mock_get):
        mock_get.return_value = mock_resp({
            'values': {'foo': 'bar'}
        })
        self.assertEqual(self.api.get('/whatever'), {'foo': 'bar'})

    @mock.patch('git_profile.bitbucket.requests.get')
    def test_get_bad_api_responses_raises_exception(self, mock_get):
        mock_get.return_value = mock_resp({}, status_code=400)
        with self.assertRaises(Exception):
            self.api.get('/whatever')

    @mock.patch('git_profile.bitbucket.requests.get')
    def test_get_calls_next_url_when_paginated_api_resp(self, mock_get):
        first_page = mock.MagicMock()
        first_page.status_code = 200
        first_page.links = {'next': {'url': 'some_url'}}

        second_page = mock.MagicMock()
        second_page.status_code = 200
        second_page.json.return_value = {'values': ['baz']}
        second_page.links = {}

        mock_get.side_effect = [first_page, second_page]

        self.assertEqual(self.api.get('/blah'), ['baz'])
