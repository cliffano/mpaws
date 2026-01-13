<img align="right" src="https://raw.github.com/cliffano/mpaws/main/avatar.jpg" alt="Avatar"/>

[![Build Status](https://github.com/cliffano/mpaws/workflows/CI/badge.svg)](https://github.com/cliffano/mpaws/actions?query=workflow%3ACI)
[![Code Scanning Status](https://github.com/cliffano/mpaws/workflows/CodeQL/badge.svg)](https://github.com/cliffano/mpaws/actions?query=workflow%3ACodeQL)
[![Dependencies Status](https://img.shields.io/librariesio/release/pypi/mpaws)](https://libraries.io/pypi/mpaws)
[![Security Status](https://snyk.io/test/github/cliffano/mpaws/badge.svg)](https://snyk.io/test/github/cliffano/mpaws)
[![Published Version](https://img.shields.io/pypi/v/mpaws.svg)](https://pypi.python.org/pypi/mpaws)
<br/>

mpaws
-----

mpaws is a Python CLI for running an AWS command across multiple profiles and multiple regions in one go.

This is a time-saver when you are managing dozens of AWS accounts and need to run the same command across all of them.

Installation
------------

    pip3 install mpaws

Usage
-----

Set an environment variable `MPAWS_PROFILES`, and another environment variable `MPAWS_REGIONS`, then run `mpaws` command:
 
    export MPAWS_PROFILES=profile1,profile2,profile3
    export MPAWS_REGIONS=us-east-1,ap-southeast-2
    mpaws ec2 describe-instances

The above command will run `aws ec2 describe-instances` command for each permutation of the AWS profiles and AWS regions, like these:
  
    AWS_PROFILE=profile1 AWS_DEFAULT_REGION=us-east-1 AWS_REGION=us-east-1 aws ec2 describe-instances
    AWS_PROFILE=profile1 AWS_DEFAULT_REGION=ap-southeast-2 AWS_REGION=ap-southeast-2 aws ec2 describe-instances
    AWS_PROFILE=profile2 AWS_DEFAULT_REGION=us-east-1 AWS_REGION=us-east-1 aws ec2 describe-instances
    AWS_PROFILE=profile2 AWS_DEFAULT_REGION=ap-southeast-2 AWS_REGION=ap-southeast-2 aws ec2 describe-instances
    AWS_PROFILE=profile3 AWS_DEFAULT_REGION=us-east-1 AWS_REGION=us-east-1 aws ec2 describe-instances
    AWS_PROFILE=profile3 AWS_DEFAULT_REGION=ap-southeast-2 AWS_REGION=ap-southeast-2 aws ec2 describe-instances

Alternatively, you can also run `mpaws` with multiple AWS profiles against a single AWS region. You can do this by setting the environment variable `MPAWS_PROFILES`, then run `mpaws` command:
 
    export MPAWS_PROFILES=profile1,profile2,profile3
    mpaws ec2 describe-instances

The above command will run `aws ec2 describe-instances` command using each AWS profile, combined with the configured AWS region (either via `AWS_DEFAULT_REGION`, `AWS_REGION`, or [the configured region within the profile definition](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-format-profile)).

Here's an example if `AWS_DEFAULT_REGION` is specified with us-east-1 as the value:

    AWS_PROFILE=profile1 AWS_DEFAULT_REGION=us-east-1 AWS_REGION=us-east-1 aws ec2 describe-instances
    AWS_PROFILE=profile2 AWS_DEFAULT_REGION=us-east-1 AWS_REGION=us-east-1 aws ec2 describe-instances-instances
    AWS_PROFILE=profile3 AWS_DEFAULT_REGION=us-east-1 AWS_REGION=us-east-1 aws ec2 describe-instances

Note that each run will also carry over the environment variables available from the original `mpaws` command run.

### Custom command

If you need to run a custom command using each profile, you can use the `_` (underscore) character which will tell mpaws to run the custom command AS-IS.

Here's an example:

    export MPAWS_PROFILES=profile1,profile2,profile3
    export MPAWS_REGIONS=us-east-1,ap-southeast-2
    mpaws _ echo \$\{AWS_PROFILE\} \$\{AWS_REGION\}

Which will run the custom command against the permutation of the AWS profiles and AWS regions:

    AWS_PROFILE=profile1 AWS_DEFAULT_REGION=us-east-1 AWS_REGION=us-east-1 echo \$\{AWS_PROFILE\} \$\{AWS_REGION\}
    AWS_PROFILE=profile1 AWS_DEFAULT_REGION=ap-southeast-2 AWS_REGION=ap-southeast-2 echo \$\{AWS_PROFILE\} \$\{AWS_REGION\}
    AWS_PROFILE=profile2 AWS_DEFAULT_REGION=us-east-1 AWS_REGION=us-east-1 echo \$\{AWS_PROFILE\} \$\{AWS_REGION\}
    AWS_PROFILE=profile2 AWS_DEFAULT_REGION=ap-southeast-2 AWS_REGION=ap-southeast-2 echo \$\{AWS_PROFILE\} \$\{AWS_REGION\}
    AWS_PROFILE=profile3 AWS_DEFAULT_REGION=us-east-1 AWS_REGION=us-east-1 echo \$\{AWS_PROFILE\} \$\{AWS_REGION\}
    AWS_PROFILE=profile3 AWS_DEFAULT_REGION=ap-southeast-2 AWS_REGION=ap-southeast-2 echo \$\{AWS_PROFILE\} \$\{AWS_REGION\}

Configuration
-------------

Ensure that the profiles specified in `MPAWS_PROFILES` are already [configured in credential file](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html). And the regions specified in `MPAWS_REGIONS`, `AWS_DEFAULT_REGION`, `AWS_REGION`, or AWS configuration are [valid regions](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/).

| Environment Variable | Mandatory | Example |
|----------------------|-----------|---------|
| MPAWS_PROFILES | Yes | profile1,profile2,profile3 |
| MPAWS_REGIONS | No | us-east-1,ap-southeast-2 |
| AWS_DEFAULT_REGION | No | us-east-1 |
| AWS_REGION | No | us-east-1 |

Colophon
--------

[Developer's Guide](https://cliffano.github.io/developers_guide.html#python)

Build reports:

* [Lint report](https://cliffano.github.io/mpaws/lint/pylint/index.html)
* [Code complexity report](https://cliffano.github.io/mpaws/complexity/radon/index.html)
* [Unit tests report](https://cliffano.github.io/mpaws/test/pytest/index.html)
* [Test coverage report](https://cliffano.github.io/mpaws/coverage/coverage/index.html)
* [Integration tests report](https://cliffano.github.io/mpaws/test-integration/pytest/index.html)
* [API Documentation](https://cliffano.github.io/mpaws/doc/sphinx/index.html)
