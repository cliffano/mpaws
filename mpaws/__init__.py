# pylint: disable=too-many-locals,broad-exception-caught
"""Python CLI for running an AWS command across multiple profiles in one go.

This CLI provides an easy way for running the same AWS command multiple times,
each time against a single AWS profile, for each of the profiles specified
in the ``MPAWS_PROFILES`` environment variable.
"""

import subprocess
import os
import sys
import click
from .logger import init


def construct_command(args: list) -> str:
    """Construct the AWS command to be executed based on the provided arguments.

    The command is prefixed with ``aws`` and the arguments are joined into a
    single string, which will be executed in the subprocess. However, if the
    first argument is ``_``, the remaining arguments are executed as a shell
    command without the ``aws`` prefix.

    :param args: Command arguments, as passed on the CLI invocation.
    :type args: list
    :returns: The command string ready to be executed in a subprocess.
    :rtype: str
    """
    if args[0] == "_":
        command = " ".join(args[1:])
    else:
        args.insert(0, "aws")
        command = " ".join(args)
    return command


def run(args: list) -> None:
    """Run mpaws by delegating AWS command executions to subprocess.

    The command is executed once for each permutation of AWS profiles
    specified in the ``MPAWS_PROFILES`` environment variable, and AWS region
    specified in either ``MPAWS_REGIONS``, ``AWS_DEFAULT_REGION``, or
    ``AWS_REGION`` environment variable.

    The other environment variables available when mpaws is executed are
    carried over to each subprocess, with ``AWS_PROFILE``,
    ``AWS_DEFAULT_REGION``, and ``AWS_REGION`` environment variables being
    set to the value of each permutation of profiles and regions.

    Standard output and standard error streams from the subprocess are
    printed to the respective stdout and stderr without any log prefix, in
    order to allow the user to grep the original output.

    Any error that occurs is trapped and counted towards the total error
    count, and the number of errors is used as the overall exit code.

    :param args: Command arguments, as passed on the CLI invocation.
    :type args: list
    :returns: This function does not return; it terminates the process via
        :func:`sys.exit` using the accumulated error count as the exit code.
    :rtype: None
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


@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.version_option(package_name="mpaws", prog_name="mpaws")
def cli(args: tuple) -> None:
    """Run an AWS command across multiple profiles in one go.

    This is the entry point registered as the ``mpaws`` console script; it
    forwards the CLI arguments to :func:`run`.

    ``args`` is captured with ``ignore_unknown_options`` enabled and typed as
    :data:`click.UNPROCESSED`, so flags meant for the underlying ``aws``
    command (or for a ``_``-prefixed shell command), such as
    ``--query`` or ``--flag1 value1``, are passed through untouched instead
    of being rejected as unknown mpaws options. mpaws' own ``--help`` and
    ``--version`` flags, being explicitly declared options, are still
    honoured.

    :param args: Command arguments captured by Click from the CLI invocation.
    :type args: tuple
    :returns: None
    :rtype: None
    """
    run(list(args))
