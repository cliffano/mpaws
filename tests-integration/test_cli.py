# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import os
import unittest
from click.testing import CliRunner
from mpaws import cli


class TestCli(unittest.TestCase):

    def setUp(self):
        os.unsetenv("MPAWS_PROFILES")
        if "MPAWS_PROFILES" in os.environ:
            os.environ.pop("MPAWS_PROFILES")
        os.unsetenv("MPAWS_REGIONS")
        if "MPAWS_REGIONS" in os.environ:
            os.environ.pop("MPAWS_REGIONS")
        os.unsetenv("AWS_DEFAULT_REGION")
        if "AWS_DEFAULT_REGION" in os.environ:
            os.environ.pop("AWS_DEFAULT_REGION")
        os.unsetenv("AWS_REGION")
        if "AWS_REGION" in os.environ:
            os.environ.pop("AWS_REGION")

    def test_cli_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage: cli [OPTIONS] [ARGS]...", result.output)
        self.assertIn("Show this message and exit.", result.output)

    def test_cli_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("mpaws, version", result.output)

    def test_cli_with_no_arg_and_no_mpaws_profiles(self):
        runner = CliRunner()
        result = runner.invoke(cli, [])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[mpaws] ERROR Please set MPAWS_PROFILES environment variable "
            "with a comma-separated list of AWS profiles to be used",
            result.output,
        )

    def test_cli_with_args_and_no_mpaws_profiles(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["ec2", "describe-instances"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[mpaws] ERROR Please set MPAWS_PROFILES environment variable "
            "with a comma-separated list of AWS profiles to be used",
            result.output,
        )

    def test_cli_without_any_region_env_var(self):
        os.environ["MPAWS_PROFILES"] = "profile1"

        runner = CliRunner()
        result = runner.invoke(cli, ["_", "echo", "hello"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[mpaws] INFO No MPAWS_REGIONS, AWS_DEFAULT_REGION, or AWS_REGION "
            "environment variable being specified",
            result.output,
        )
        self.assertIn(
            "[mpaws] INFO Using region information associated with the profiles",
            result.output,
        )

    def test_cli_with_custom_shell_command_and_single_profile_and_region(self):
        os.environ["MPAWS_PROFILES"] = "profile1"
        os.environ["MPAWS_REGIONS"] = "us-east-1"

        runner = CliRunner()
        result = runner.invoke(cli, ["_", "echo", "${AWS_PROFILE}", "${AWS_REGION}"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[mpaws] INFO Environment variables: AWS_PROFILE=profile1 "
            "AWS_DEFAULT_REGION=us-east-1 AWS_REGION=us-east-1",
            result.output,
        )
        self.assertIn("profile1 us-east-1", result.output)

    def test_cli_with_custom_shell_command_and_multiple_profiles_and_regions(self):
        os.environ["MPAWS_PROFILES"] = "profile1,profile2"
        os.environ["MPAWS_REGIONS"] = "us-east-1,ap-southeast-2"

        runner = CliRunner()
        result = runner.invoke(cli, ["_", "echo", "${AWS_PROFILE}", "${AWS_REGION}"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("profile1 us-east-1", result.output)
        self.assertIn("profile1 ap-southeast-2", result.output)
        self.assertIn("profile2 us-east-1", result.output)
        self.assertIn("profile2 ap-southeast-2", result.output)

    def test_cli_falls_back_to_aws_default_region(self):
        os.environ["MPAWS_PROFILES"] = "profile1"
        os.environ["AWS_DEFAULT_REGION"] = "us-west-2"

        runner = CliRunner()
        result = runner.invoke(cli, ["_", "echo", "${AWS_PROFILE}", "${AWS_REGION}"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[mpaws] INFO Environment variables: AWS_PROFILE=profile1 "
            "AWS_DEFAULT_REGION=us-west-2 AWS_REGION=us-west-2",
            result.output,
        )
        self.assertIn("profile1 us-west-2", result.output)

    def test_cli_falls_back_to_aws_region(self):
        os.environ["MPAWS_PROFILES"] = "profile1"
        os.environ["AWS_REGION"] = "eu-west-1"

        runner = CliRunner()
        result = runner.invoke(cli, ["_", "echo", "${AWS_PROFILE}", "${AWS_REGION}"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[mpaws] INFO Environment variables: AWS_PROFILE=profile1 "
            "AWS_DEFAULT_REGION=eu-west-1 AWS_REGION=eu-west-1",
            result.output,
        )
        self.assertIn("profile1 eu-west-1", result.output)

    def test_cli_with_flags_forwarded_to_custom_shell_command(self):
        os.environ["MPAWS_PROFILES"] = "profile1"
        os.environ["MPAWS_REGIONS"] = "us-east-1"

        runner = CliRunner()
        result = runner.invoke(
            cli, ["_", "echo", "--flag1", "value1", "--flag2", "value2"]
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "[mpaws] INFO Command: echo --flag1 value1 --flag2 value2",
            result.output,
        )
        self.assertIn("--flag1 value1 --flag2 value2", result.output)

    def test_cli_with_command_not_found_counts_error(self):
        os.environ["MPAWS_PROFILES"] = "profile1"
        os.environ["MPAWS_REGIONS"] = "us-east-1"

        runner = CliRunner()
        result = runner.invoke(cli, ["_", "some-inexisting-command"])

        self.assertEqual(result.exit_code, 1)
        self.assertIn("[mpaws] ERROR Standard error:", result.output)
        self.assertIn("some-inexisting-command", result.output)

    def test_cli_with_no_arg_and_mpaws_profiles_set(self):
        os.environ["MPAWS_PROFILES"] = "profile1"

        runner = CliRunner()
        result = runner.invoke(cli, [])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIsInstance(result.exception, IndexError)
