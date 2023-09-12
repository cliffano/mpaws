# pylint: disable=too-many-locals,broad-exception-caught
"""
mpaws
=====
Execute AWS CLI across multiple profiles in one go.
"""
import subprocess
import os
import sys
import click
from .logger import init

def run(args: str) -> None:
    """Run mpaws by delegating aws commands to subprocesses,
    one for each AWS profile included in MPAWS_PROFILES environment variable.
    """

    logger = init()

    command_args = ' '.join(args)
    command = f'aws {command_args}'

    if 'MPAWS_PROFILES' in os.environ:

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

            except Exception as exception:
                logger.error(f'An exception occurred: {str(exception)}')

    else:
        logger.warning('Please set MPAWS_PROFILES environment variable' \
                       'with a comma-separated list of AWS profiles to be used')

@click.command()
@click.argument('args', nargs=-1)
def cli(args: str) -> None:
    """Run an AWS command across multiple profiles in one go."""
    run(args)
