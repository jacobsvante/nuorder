# Changelog

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
