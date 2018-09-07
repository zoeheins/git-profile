from unittest import mock

import requests


def mock_resp(resp, status_code=200):
    response = mock.Mock(spec=requests.Response)
    response.status_code = status_code
    response.links = None
    response.json.return_value = resp
    return response
