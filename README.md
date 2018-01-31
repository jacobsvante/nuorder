# nuorder

[![Travis CI build status (Linux)](https://travis-ci.org/jmagnusson/nuorder.svg?branch=master)](https://travis-ci.org/jmagnusson/nuorder)
[![PyPI version](https://img.shields.io/pypi/v/nuorder.svg)](https://pypi.python.org/pypi/nuorder/)
[![License](https://img.shields.io/pypi/l/nuorder.svg)](https://pypi.python.org/pypi/nuorder/)
[![Available as wheel](https://img.shields.io/pypi/wheel/nuorder.svg)](https://pypi.python.org/pypi/nuorder/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/nuorder.svg)](https://pypi.python.org/pypi/nuorder/)
[![PyPI status (alpha/beta/stable)](https://img.shields.io/pypi/status/nuorder.svg)](https://pypi.python.org/pypi/nuorder/)
[![Coverage Status](https://coveralls.io/repos/github/jmagnusson/nuorder/badge.svg?branch=master)](https://coveralls.io/github/jmagnusson/nuorder?branch=master)

Make requests to NuOrder's wholesale API


## Install

Python 3+ should be supported, but only Python 3.5 & 3.6 has actually been tested. So please ensure that you're on the right platform.

For CLI access:
```bash
$ pip install nuorder[cli]
```

For programmatic access only:
```bash
$ pip install nuorder
```


## 2. CLI access

Create a settings file in `~/.config/nuorder.ini`, with data from the API management section. `hostname` is usually `wholesale.sandbox1.nuorder.com` for sandbox and `wholesale.nuorder.com` for production. `app_name` is whatever you want it to be. `sandbox` is the default config section used, but can be overridden in all API calls, with `--config-section` (or `-c`). For more info run `nuorder --help`.

```ini
[sandbox]
hostname = wholesale.sandbox1.nuorder.com
app_name = My app
consumer_key = QdaGd4ppfXTPEaxnjz4C
consumer_secret = ZvbKP5jxL0iXJ2p7zNRsBzG9vo8XdSIVLb1fMkWFX55dsKTL
oauth_token = ; Will be created in next step if needed
oauth_token_secret = ; Will be created in next step if needed
```

## Getting an OAuth token and secret

```bash
$ nuorder initiate
Got response: {
  "oauth_callback_confirmed": true,
  "oauth_token_secret": "ybuXkNIXMvWPToeckJZgIglTC",
  "oauth_token": "ka6WdMG3znnQeGVb"
}
Now go to the API management section of NuOrder's admin page and approve the pending application that matches the details above. Copy the verification code that was shown in the pop-up after the approval was made and paste it here.
Verification code [paste and press Enter]: dwjwiJJhIs1F9Bv9
Success! Final OAuth token and secret to use below. Remember to save them in the INI config.
{
  "oauth_token_secret": "CFVUGtkbNG8JwaU4XPo0GKj2JZwMnepwhctqUrdsdAFC9DUUGZQXvR8s4J",
  "oauth_token": "INUHZ66ihxffUKhg86tRjYy"
}
```

Now you just have to put `oauth_token_secret` and `oauth_token` in the config previously created and you should be good to go.

## Making API calls from the CLI

Now that the config is set up you can begin to make API requests.

Some examples below:

```bash
# Get all company codes
nuorder get /api/companies/codes/list

# Creating an order
cat my-order-payload.json | nuorder put /api/order/new --data -
```

## Making API calls programmatically

Example:

```python
import nuorder
NUORDER_CONFIG = {
    'hostname': 'wholesale.sandbox1.nuorder.com',
    'consumer_key': 'fake_consumer_key',
    'consumer_secret': 'fake_consumer_secret',
    'oauth_token': 'fake_oauth_token',
    'oauth_token_secret': 'fake_oauth_token_secret',
}
nu = nuorder.NuOrder(
    **NUORDER_CONFIG,
)
companies = nu.get('/api/companies/codes/list')
```
