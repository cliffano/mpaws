<img align="right" src="https://raw.github.com/cliffano/mpaws/main/avatar.jpg" alt="Avatar"/>

[![Build Status](https://github.com/cliffano/mpaws/workflows/CI/badge.svg)](https://github.com/cliffano/mpaws/actions?query=workflow%3ACI)
[![Security Status](https://snyk.io/test/github/cliffano/mpaws/badge.svg)](https://snyk.io/test/github/cliffano/mpaws)
[![Published Version](https://img.shields.io/pypi/v/mpaws.svg)](https://pypi.python.org/pypi/mpaws)
<br/>

mpaws
-------

mpaws is a Python CLI for generating report of SSL certificates from multiple endpoints specified in a YAML configuration.

Installation
------------

    pip3 install mpaws

Usage
-----

Create a configuration file, e.g. `mpaws.yaml`:

    ---
    endpoints:
      - host: apple.com
        port: 443
      - host: google.com
        port: 443
      - host: microsoft.com
        port: 443
 
And then run `mpaws` CLI and pass the configuration file path:

    mpaws --conf-file mpaws.yaml

It will write the log messages to stdout:

    [mpaws] INFO Loading configuration file mpaws.yaml
    [mpaws] INFO TODO

Configuration
-------------

Configuration properties:

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `endpoints[]` | Array | A list of one or more endpoints with ... | |
| `endpoints[].host` | String | The name of the tagset. | `apple.com` |
| `endpoints[].port` | String | The name of the tagset. | `443` |

Colophon
--------

[Developer's Guide](https://cliffano.github.io/developers_guide.html#python)

Build reports:

* [Lint report](https://cliffano.github.io/mpaws/lint/pylint/index.html)
* [Code complexity report](https://cliffano.github.io/mpaws/complexity/wily/index.html)
* [Unit tests report](https://cliffano.github.io/mpaws/test/pytest/index.html)
* [Test coverage report](https://cliffano.github.io/mpaws/coverage/coverage/index.html)
* [Integration tests report](https://cliffano.github.io/mpaws/test-integration/pytest/index.html)
* [API Documentation](https://cliffano.github.io/mpaws/doc/sphinx/index.html)
