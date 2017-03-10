import termcolor
import json
import logging
import sys

import argh

import nuorder


def _failure(err):
    return termcolor.colored(str(err), 'red')


def _set_log_level(log_level):
    nuorder.logger.setLevel(getattr(logging, log_level.upper()))


@argh.wrap_errors([nuorder.config.ConfigKeyMissing], processor=_failure)
@argh.arg('-c', '--config-section')
def initiate(
    hostname: 'E.g. wholesale.sandbox1.nuorder.com for sandbox' = None,
    consumer_key: 'The consumer key to use' = None,
    consumer_secret: 'The oauth shared secret to use' = None,
    app_name: 'The application name.' = None,
    config_section: 'The name of the config section to get settings from.' = 'sandbox',
    log_level: 'The log level to use.' = 'WARNING',
    dry_run: "Don't actually run command, just show what would be run." = False
):
    """Make GET requests to NuOrder"""
    _set_log_level(log_level)

    request_args = dict(
        method='GET',
        hostname=hostname,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        config_section=config_section,
        app_name=app_name,
        dry_run=dry_run,
    )
    resp_json = nuorder.request(endpoint='/api/initiate', **request_args)
    resp_text = json.dumps(resp_json, indent=2)

    if 'request_error' in resp_json:
        sys.exit(_failure(resp_text))

    print('Got response:', resp_text, file=sys.stderr)

    if dry_run:
        sys.exit()

    print(
        "Now go to the API management section of NuOrder's admin page "
        "and approve the pending application that matches the details above. "
        "Copy the verification code that was shown in the pop-up after the "
        "approval was made and paste it here.",
        file=sys.stderr
    )
    verifier = input("Verification code [paste and press Enter]: ")

    resp_json = nuorder.request(
        endpoint='/api/token',
        **request_args,
        oauth_token=resp_json['oauth_token'],
        oauth_token_secret=resp_json['oauth_token_secret'],
        oauth_verifier=verifier,
    )

    if 'request_error' in resp_json:
        sys.exit(_failure(json.dumps(resp_json, indent=2)))

    print(
        'Success! Final OAuth token and secret to use below. '
        'Remember to save them in the INI config.',
        file=sys.stderr
    )
    return json.dumps(resp_json, indent=2)


@argh.wrap_errors([nuorder.config.ConfigKeyMissing], processor=_failure)
@argh.arg('-c', '--config-section')
def delete(
    endpoint: 'The endpoint to interact with.',
    hostname: 'E.g. wholesale.sandbox1.nuorder.com for sandbox' = None,
    consumer_key: 'The consumer key to use' = None,
    consumer_secret: 'The oauth shared secret to use' = None,
    oauth_token: 'OAuth token' = None,
    oauth_token_secret: 'OAuth token secret' = None,
    config_section: 'The name of the config section to get settings from.' = 'sandbox',
    log_level: 'The log level to use.' = 'WARNING',
    dry_run: "Don't actually run command, just show what would be run." = False
):
    """Make a DELETE request to NuOrder"""
    _set_log_level(log_level)
    resp_json = nuorder.request(
        method='DELETE',
        endpoint=endpoint,
        hostname=hostname,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret,
        config_section=config_section,
        dry_run=dry_run,
    )
    return json.dumps(resp_json, indent=2)


@argh.wrap_errors([nuorder.config.ConfigKeyMissing], processor=_failure)
@argh.arg('-c', '--config-section')
def get(
    endpoint: 'The endpoint to interact with.',
    hostname: 'E.g. wholesale.sandbox1.nuorder.com for sandbox' = None,
    consumer_key: 'The consumer key to use' = None,
    consumer_secret: 'The oauth shared secret to use' = None,
    oauth_token: 'OAuth token' = None,
    oauth_token_secret: 'OAuth token secret' = None,
    config_section: 'The name of the config section to get settings from.' = 'sandbox',
    log_level: 'The log level to use.' = 'WARNING',
    dry_run: "Don't actually run command, just show what would be run." = False
):
    """Make a GET request to NuOrder"""
    _set_log_level(log_level)
    resp_json = nuorder.request(
        method='GET',
        endpoint=endpoint,
        hostname=hostname,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret,
        config_section=config_section,
        dry_run=dry_run,
    )
    return json.dumps(resp_json, indent=2)


@argh.wrap_errors([nuorder.config.ConfigKeyMissing], processor=_failure)
@argh.arg('-c', '--config-section')
def post(
    endpoint: 'The endpoint to interact with.',
    hostname: 'E.g. wholesale.sandbox1.nuorder.com for sandbox' = None,
    consumer_key: 'The consumer key to use' = None,
    consumer_secret: 'The oauth shared secret to use' = None,
    oauth_token: 'OAuth token' = None,
    oauth_token_secret: 'OAuth token secret' = None,
    data: 'The data to send along with POST/PUT. If `-` then read from stdin.' = None,
    config_section: 'The name of the config section to get settings from.' = 'sandbox',
    log_level: 'The log level to use.' = 'WARNING',
    dry_run: "Don't actually run command, just show what would be run." = False
):
    """Make a PUT request to NuOrder"""
    _set_log_level(log_level)
    resp_json = nuorder.request(
        method='POST',
        endpoint=endpoint,
        hostname=hostname,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret,
        data=data,
        config_section=config_section,
        dry_run=dry_run,
    )
    return json.dumps(resp_json, indent=2)


@argh.wrap_errors([nuorder.config.ConfigKeyMissing], processor=_failure)
@argh.arg('-c', '--config-section')
def put(
    endpoint: 'The endpoint to interact with.',
    hostname: 'E.g. wholesale.sandbox1.nuorder.com for sandbox' = None,
    consumer_key: 'The consumer key to use' = None,
    consumer_secret: 'The oauth shared secret to use' = None,
    oauth_token: 'OAuth token' = None,
    oauth_token_secret: 'OAuth token secret' = None,
    data: 'The data to send along with POST/PUT. If `-` then read from stdin.' = None,
    config_section: 'The name of the config section to get settings from.' = 'sandbox',
    log_level: 'The log level to use.' = 'WARNING',
    dry_run: "Don't actually run command, just show what would be run." = False
):
    """Make a PUT request to NuOrder"""
    _set_log_level(log_level)
    resp_json = nuorder.request(
        method='PUT',
        endpoint=endpoint,
        hostname=hostname,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        oauth_token=oauth_token,
        oauth_token_secret=oauth_token_secret,
        data=data,
        config_section=config_section,
        dry_run=dry_run,
    )
    return json.dumps(resp_json, indent=2)


command_parser = argh.ArghParser(description=nuorder.__doc__)
command_parser.add_commands([
    initiate,
    get,
    delete,
    post,
    put,
])
main = command_parser.dispatch
