# pylint: disable=too-many-locals,broad-exception-caught
"""
mpaws
=====
Python CLI for running an AWS command across multiple profiles in one go.

This CLI provides an easy way for running the same AWS command multiple times,
each time against a single AWS profile, for each of the profiles specified
in MPAWS_PROFILES environment variable.
"""
import subprocess
import os
import sys
import click
from .logger import init

def run(args: str) -> None:
    """Run mpaws by delegating aws command executions to subprocess,
    once for each AWS profile specified in MPAWS_PROFILES environment variable.
    The environment variables available when mpaws is executed, will be
    carried over to each subprocess, with AWS_PROFILE environment variable
    being set to the value of each profile.

    Standard output and standard error streams from the subprocess will be
    printed to the respective stdout and stderr without any log prefix, in
    order to allow user to grep the original output.

    Any error that occurs will be trapped
    """

    logger = init()

    command_args = ' '.join(args)
    command = f'aws {command_args}'

    if 'MPAWS_PROFILES' in os.environ:

        error_count = 0
        aws_profiles = os.getenv('MPAWS_PROFILES').split(',')

        for aws_profile in aws_profiles:

            # Copy the current environment variables, to be used by each subprocess
            env_vars = os.environ.copy()
            # Set AWS_PROFILE environment variable with the current AWS profile
            env_vars['AWS_PROFILE'] = aws_profile

            logger.info('----------------------------------------')
            logger.info(f'AWS_PROFILE={aws_profile} {command}')

            try:
                # Run the command using subprocess with the modified environment variables
                result = subprocess.run(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=env_vars,
                    check=False
                )

                if result.stdout:
                    logger.info('Standard output:')
                    print(result.stdout, file=sys.stdout)
                    logger.info(f'Exit code: {result.returncode}')

                if result.stderr:
                    logger.error('Standard error:')
                    print(result.stderr, file=sys.stderr)
                    logger.error(f'Exit code: {result.returncode}')
                    error_count += 1

            except Exception as exception:
                logger.error(f'An exception occurred: {str(exception)}')
                error_count += 1

        sys.exit(error_count if error_count >= 1 else 0)

    else:
        logger.warning('Please set MPAWS_PROFILES environment variable ' \
                       'with a comma-separated list of AWS profiles to be used')

@click.command()
@click.argument('args', nargs=-1)
def cli(args: str) -> None:
    """Run an AWS command across multiple profiles in one go."""
    run(args)
