import pytest


@pytest.fixture
def default_request_kw():
    return {
        'hostname': 'wholesale.sandbox1.nuorder.com',
        'consumer_key': 'fake_consumer_key',
        'consumer_secret': 'fake_consumer_secret',
        'oauth_token': 'fake_oauth_token',
        'oauth_token_secret': 'fake_oauth_token_secret',
        'app_name': 'fake_app_name',
    }
