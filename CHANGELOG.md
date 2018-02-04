# Changelog

## 1.1.1 (2018-02-04)

* Make the `data` arg optional for POST/PUT requests
* Previously we returned a "request error" when response from NuOrder couldn't be processed as JSON. Instead of `{"request_error": [response text]}` we're now returning the more descriptive `{"response_status_code": [HTTP status code], "response_text": [response text], "json_decode_error_details": [JSONDecodeError details]}`, or `{}` if there was no response body (which of course would fail to parse as JSON).

## 1.1.0 (2018-01-31)

* Refactor to use class, for easier repeated access
* New CLI named `interact`, for more easily interacting with the nuorder API,
  using the IPython REPL.
* `requests` is now the only dependency in the base package. `argh` and `termcolor` are now installed by issuing `pip install nuorder[cli]`
* Limit config initialization to CLI, to enable programmatic usage


## 1.0.1 (2017-04-19)

* Support gzipped data transfers for POST and PUT requests with the -g flag
* List python 3.6 as supported

## 1.0.0 (2017-03-10)

* Initial version
