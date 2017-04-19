import pytest


@pytest.fixture
def default_request_kw():
    return {
        'hostname': 'wholesale.sandbox1.nuorder.com',
        'consumer_key': '',
        'consumer_secret': '',
        'oauth_token': '',
        'oauth_token_secret': '',
        'app_name': '',
    }
