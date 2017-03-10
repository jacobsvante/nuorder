# nuorder

[![Travis CI build status (Linux)](https://travis-ci.org/jmagnusson/nuorder.svg?branch=master)](https://travis-ci.org/jmagnusson/nuorder)
[![PyPI version](https://img.shields.io/pypi/v/nuorder.svg)](https://pypi.python.org/pypi/nuorder/)
[![Downloads from PyPI per month](https://img.shields.io/pypi/dm/nuorder.svg)](https://pypi.python.org/pypi/nuorder/)
[![License](https://img.shields.io/pypi/l/nuorder.svg)](https://pypi.python.org/pypi/nuorder/)
[![Available as wheel](https://img.shields.io/pypi/wheel/nuorder.svg)](https://pypi.python.org/pypi/nuorder/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/nuorder.svg)](https://pypi.python.org/pypi/nuorder/)
[![PyPI status (alpha/beta/stable)](https://img.shields.io/pypi/status/nuorder.svg)](https://pypi.python.org/pypi/nuorder/)
[![Coverage Status](https://coveralls.io/repos/github/jmagnusson/nuorder/badge.svg?branch=master)](https://coveralls.io/github/jmagnusson/nuorder?branch=master)
[![Code Health](https://landscape.io/github/jmagnusson/nuorder/master/landscape.svg?style=flat)](https://landscape.io/github/jmagnusson/nuorder/master)

Make requests to NuOrder's wholesale API


## 1. Install

Python 2 is not supported. Only tested with Python 3.5, so make sure it's installed with the right version.

```bash
$ pip install nuorder
```


## 2. Creating the config

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

## 3. Getting OAuth token and secret

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

## 4. Making API calls

Now that the config is set up you can begin to make API requests.

Some examples below:

```bash
# Getting all companies
nuorder get /api/companies/codes/list

# Creating an order
cat my-order-payload.json | nuorder put /api/order/new --data -
```
