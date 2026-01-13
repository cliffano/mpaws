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


def construct_command(args: list) -> str:
    """Construct the AWS command to be executed based on the provided arguments.
    The command will be prefixed with "aws" and the arguments are joined into a single
    string, which will be executed in the subprocess.
    But if the first arg is _, it will be executed as a shell command
    without the "aws" prefix.
    """
    if args[0] == "_":
        command = " ".join(args[1:])
    else:
        args.insert(0, "aws")
        command = " ".join(args)
    return command


def run(args: list) -> None:
    """Run mpaws by delegating aws command executions to subprocess,
    once for each permutation of AWS profiles specified in MPAWS_PROFILES
    environment variable, and AWS region specified in either MPAWS_REGIONS,
    AWS_DEFAULT_REGION, or AWS_REGION environment variable.
    The other environment variables available when mpaws is executed, will be
    carried over to each subprocess, with AWS_PROFILE, AWS_DEFAULT_REGION, and
    AWS_REGION environment variables being set to the value of each permutation
    of profiles and regions.

    Standard output and standard error streams from the subprocess will be
    printed to the respective stdout and stderr without any log prefix, in
    order to allow user to grep the original output.

    Any error that occurs will be trapped and calculated towards the total
    errors count, and the number of errors is used as the overall exit code.
    """

    logger = init()

    aws_profiles = []
    if "MPAWS_PROFILES" in os.environ:
        aws_profiles = os.getenv("MPAWS_PROFILES").split(",")
    else:
        logger.error(
            "Please set MPAWS_PROFILES environment variable "
            "with a comma-separated list of AWS profiles to be used"
        )
        sys.exit(0)

    aws_regions = []
    if "MPAWS_REGIONS" in os.environ:
        aws_regions = os.getenv("MPAWS_REGIONS").split(",")
    elif "AWS_DEFAULT_REGION" in os.environ:
        aws_regions = [os.getenv("AWS_DEFAULT_REGION")]
    elif "AWS_REGION" in os.environ:
        aws_regions = [os.getenv("AWS_REGION")]
    else:
        logger.info(
            "No MPAWS_REGIONS, AWS_DEFAULT_REGION, or AWS_REGION "
            "environment variable being specified"
        )
        logger.info("Using region information associated with the profiles")

    command = construct_command(args)
    error_count = 0

    for aws_profile in aws_profiles:
        for aws_region in aws_regions:

            # Copy the current environment variables, to be used by each subprocess
            env_vars = os.environ.copy()
            # Set AWS_PROFILE environment variable with the current AWS profile
            env_vars["AWS_PROFILE"] = aws_profile
            # Set AWS_DEFAULT_REGION and AWS_REGION environment variables
            # with the current AWS region
            env_vars["AWS_DEFAULT_REGION"] = aws_region
            env_vars["AWS_REGION"] = aws_region

            logger.info("----------------------------------------")
            logger.info(
                f"Environment variables: AWS_PROFILE={aws_profile} AWS_DEFAULT_REGION={aws_region} "
                f"AWS_REGION={aws_region}"
            )
            logger.info(f"Command: {command}")

            try:
                # Run the command using subprocess with the modified environment variables
                result = subprocess.run(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=env_vars,
                    check=False,
                )

                if result.stdout:
                    logger.info("Standard output:")
                    print(result.stdout, file=sys.stdout)
                    logger.info(f"Exit code: {result.returncode}")

                if result.stderr:
                    logger.error("Standard error:")
                    print(result.stderr, file=sys.stderr)
                    logger.error(f"Exit code: {result.returncode}")
                    error_count += 1

            except Exception as exception:
                logger.error(f"An exception occurred: {str(exception)}")
                error_count += 1

    sys.exit(error_count if error_count >= 1 else 0)


@click.command()
@click.argument("args", nargs=-1)
@click.version_option(package_name="certilizer", prog_name="certilizer")
def cli(args: tuple) -> None:
    """Run an AWS command across multiple profiles in one go."""
    run(list(args))
