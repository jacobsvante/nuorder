"""Package for making HTTP requests to the NuOrder API

It's recommended to put hostname and consumer/oauth settings in an INI-style
file at the location ~/.config/nuorder.ini. This way you don't have to
put them in for every request.

        [sandbox]
        hostname = wholesale.sandbox1.nuorder.com
        consumer_key = QDaGd4ppfXTPEaxnjz4C
        consumer_secret = ZvbKP5jxL0iBJ2p7zNRsBzG9vo8XdSIVLb1fMkWFX55dsKTL
        oauth_token = 74SCldgh0DfBufxKJTlEe
        oauth_token_secret = Eb6haktmLIeTYO0LuyCktJNADpYPMnvo6rWWKOs6oh1WJH
        app_name = My app

Then you can simply issue a request to their API like this::

    nuorder get /api/companies/codes/list

Please note that the config section name `sandbox` is the
default and can be overridden by passing in `-c <name>`.
Useful when one wants to make calls to both sandbox and production
environments."""
import functools
import hashlib
import hmac
import json
import logging
import uuid
import sys
from datetime import datetime

import requests

from . import config

__all__ = [
    'config',
    'logger',
    'request',
]

logging.basicConfig()
logger = logging.getLogger('nuorder')


def raise_for_status_with_body(resp):
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        raise RuntimeError('{}:\n\n{}'.format(resp.status_code, resp.text))


def request(
    method: 'The method to use (e.g. GET|POST|PUT|DELETE)',
    endpoint: 'The endpoint to interact with.',
    hostname: 'E.g. wholesale.sandbox1.nuorder.com for sandbox' = None,
    consumer_key: 'The consumer key to use' = None,
    consumer_secret: 'The oauth shared secret to use' = None,
    oauth_token='',
    oauth_token_secret='',
    oauth_verifier='',
    data: 'The data to send along with POST/PUT' = None,
    app_name: 'The application name.' = None,
    config_section: 'The name of the config section to get settings from.' = 'sandbox',
    nonce: 'The nonce to use. Defaults to 16 random alphanumericals.' = None,
    timestamp: 'The timestamp to use. Defaults to local now.' = None,
    dry_run: "Don't actually run command if True" = False
):
    c = functools.partial(config.get, config_section)

    is_initiate_url = endpoint == '/api/initiate'
    method = method.upper()
    hostname = hostname or c('hostname')
    consumer_key = consumer_key or c('consumer_key')
    consumer_secret = consumer_secret or c('consumer_secret')
    oauth_token = oauth_token or c('oauth_token', required=not is_initiate_url)
    oauth_token_secret = oauth_token_secret or c(
        'oauth_token_secret',
        required=(not is_initiate_url)
    )
    app_name = app_name or c('app_name', required=is_initiate_url)

    if data == '-':
        data = ''.join(sys.stdin)

    url = 'https://{}{}'.format(hostname, endpoint)
    base_string_tmpl = '{method}{url}?oauth_consumer_key={consumer_key}&oauth_token={oauth_token}&oauth_timestamp={timestamp}&oauth_nonce={nonce}&oauth_version=1.0&oauth_signature_method=HMAC-SHA1'
    authorization_header_tmpl = 'OAuth oauth_consumer_key="{consumer_key}",oauth_timestamp="{timestamp}",oauth_nonce="{nonce}",oauth_version="1.0",oauth_signature_method="HMAC-SHA1",oauth_token="{oauth_token}",oauth_signature="{signature}",application_name="{app_name}"'

    if is_initiate_url:
        base_string_tmpl += '&oauth_callback=oob'
        authorization_header_tmpl += ',oauth_callback="oob"'
    if oauth_verifier:
        base_string_tmpl += '&oauth_verifier=' + oauth_verifier
        authorization_header_tmpl += ',oauth_verifier="{}"'.format(oauth_verifier)

    if timestamp is None:
        timestamp = int(datetime.now().timestamp())

    if nonce is None:
        nonce = uuid.uuid4().hex[0:16]

    hmac_text = base_string_tmpl.format(
        method=method,
        url=url,
        oauth_token=oauth_token,
        consumer_key=consumer_key,
        nonce=nonce,
        timestamp=timestamp
    ).encode('utf-8')

    hmac_key = '{}&{}'.format(
        consumer_secret,
        oauth_token_secret
    ).encode('utf-8')

    obj = hmac.new(hmac_key, digestmod=hashlib.sha1)
    obj.update(hmac_text)
    signature = obj.hexdigest()

    logger.debug('HMAC text: {}'.format(hmac_text))
    logger.debug('HMAC key: {}'.format(hmac_key))
    logger.debug('HMAC hash: {}'.format(signature))

    authorization_header = authorization_header_tmpl.format(
        nonce=nonce,
        timestamp=timestamp,
        consumer_key=consumer_key,
        signature=signature,
        oauth_token=oauth_token,
        app_name=app_name,
    )

    headers = {
        'Authorization': authorization_header,
        'Content-Type': 'application/json',
    }

    logger.debug(headers)
    if dry_run:
        return {
            'would_do': {
                'method': method,
                'url': url,
                'headers': headers,
                'data': data,
            }
        }
    else:
        logger.info('{} {}'.format(method, url))
        resp = requests.request(method, url, headers=headers, data=data)
        raise_for_status_with_body(resp)
        logger.info('Returned HTTP status {}'.format(resp.status_code))
        try:
            return resp.json()
        except json.decoder.JSONDecodeError:
            return {'request_error': resp.text}
