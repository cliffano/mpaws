<img align="right" src="https://raw.github.com/cliffano/mpaws/main/avatar.jpg" alt="Avatar"/>

[![Build Status](https://github.com/cliffano/mpaws/workflows/CI/badge.svg)](https://github.com/cliffano/mpaws/actions?query=workflow%3ACI)
[![Security Status](https://snyk.io/test/github/cliffano/mpaws/badge.svg)](https://snyk.io/test/github/cliffano/mpaws)
[![Published Version](https://img.shields.io/pypi/v/mpaws.svg)](https://pypi.python.org/pypi/mpaws)
<br/>

mpaws
-----

mpaws is a Python CLI for running an AWS command across multiple profiles in one go.

This is a time-saver when you are managing dozens of AWS accounts and need to run the same command across all of them.

Installation
------------

    pip3 install mpaws

Usage
-----

Set an environment variable `MPAWS_PROFILES`, then run `mpaws` command:
 
    export MPAWS_PROFILES=profile1,profile2,profile3,profile4,profile5
    mpaws s3 ls

The above command will run `aws s3 ls` command for AWS profile `profile1`, `profile2`, up to `profile5`. A bit like this:
  
    AWS_PROFILE=profile1 aws s3 ls
    AWS_PROFILE=profile2 aws s3 ls

Each run will also carry over the environment variables available when the original `mpaws` command was run.

Configuration
-------------

Ensure that the profiles specified in `MPAWS_PROFILES` are already [configured in credential file](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

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
