# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch
import unittest.mock
import unittest
from click.testing import CliRunner
from mpaws import cli, construct_command, run


class TestMpaws(unittest.TestCase):

    def test_aws_command_without_flags(self):

        args = ["ec2", "describe-instances"]

        self.assertEqual(construct_command(args), "aws ec2 describe-instances")

    def test_aws_command_with_flags(self):

        args = ["ec2", "describe-instances", "--query", "foo"]

        self.assertEqual(
            construct_command(args), "aws ec2 describe-instances --query foo"
        )

    def test_aws_command_with_multiple_flags(self):

        args = ["ec2", "describe-instances", "--flag1", "value1", "--flag2", "value2"]

        self.assertEqual(
            construct_command(args),
            "aws ec2 describe-instances --flag1 value1 --flag2 value2",
        )

    def test_underscore_prefixed_shell_command(self):

        args = ["_", "echo", "${AWS_PROFILE}", "${AWS_REGION}"]

        self.assertEqual(construct_command(args), "echo ${AWS_PROFILE} ${AWS_REGION}")

    @patch("mpaws.init")
    @patch.dict("os.environ", {}, clear=True)
    def test_run_without_mpaws_profiles_logs_error_and_exits(self, func_init):

        mock_logger = unittest.mock.Mock()
        func_init.return_value = mock_logger

        with self.assertRaises(SystemExit) as context:
            run(["ec2", "describe-instances"])

        self.assertEqual(context.exception.code, 0)
        mock_logger.error.assert_called_once_with(
            "Please set MPAWS_PROFILES environment variable "
            "with a comma-separated list of AWS profiles to be used"
        )

    @patch("mpaws.subprocess.run")
    @patch("mpaws.init")
    @patch.dict("os.environ", {"MPAWS_PROFILES": "profile1"}, clear=True)
    def test_run_without_any_region_env_var_logs_info_and_skips_execution(
        self, func_init, func_subprocess_run
    ):

        mock_logger = unittest.mock.Mock()
        func_init.return_value = mock_logger

        with self.assertRaises(SystemExit) as context:
            run(["ec2", "describe-instances"])

        self.assertEqual(context.exception.code, 0)
        func_subprocess_run.assert_not_called()
        mock_logger.info.assert_any_call(
            "No MPAWS_REGIONS, AWS_DEFAULT_REGION, or AWS_REGION "
            "environment variable being specified"
        )
        mock_logger.info.assert_any_call(
            "Using region information associated with the profiles"
        )

    @patch("mpaws.subprocess.run")
    @patch("mpaws.init")
    @patch.dict(
        "os.environ",
        {"MPAWS_PROFILES": "profile1", "MPAWS_REGIONS": "us-east-1"},
        clear=True,
    )
    def test_run_uses_mpaws_regions_when_set(self, func_init, func_subprocess_run):

        mock_logger = unittest.mock.Mock()
        func_init.return_value = mock_logger
        func_subprocess_run.return_value = unittest.mock.Mock(
            stdout="", stderr="", returncode=0
        )

        with self.assertRaises(SystemExit) as context:
            run(["ec2", "describe-instances"])

        self.assertEqual(context.exception.code, 0)
        _, kwargs = func_subprocess_run.call_args
        self.assertEqual(kwargs["env"]["AWS_PROFILE"], "profile1")
        self.assertEqual(kwargs["env"]["AWS_DEFAULT_REGION"], "us-east-1")
        self.assertEqual(kwargs["env"]["AWS_REGION"], "us-east-1")

    @patch("mpaws.subprocess.run")
    @patch("mpaws.init")
    @patch.dict(
        "os.environ",
        {"MPAWS_PROFILES": "profile1", "AWS_DEFAULT_REGION": "us-west-2"},
        clear=True,
    )
    def test_run_falls_back_to_aws_default_region(self, func_init, func_subprocess_run):

        mock_logger = unittest.mock.Mock()
        func_init.return_value = mock_logger
        func_subprocess_run.return_value = unittest.mock.Mock(
            stdout="", stderr="", returncode=0
        )

        with self.assertRaises(SystemExit):
            run(["ec2", "describe-instances"])

        _, kwargs = func_subprocess_run.call_args
        self.assertEqual(kwargs["env"]["AWS_DEFAULT_REGION"], "us-west-2")
        self.assertEqual(kwargs["env"]["AWS_REGION"], "us-west-2")

    @patch("mpaws.subprocess.run")
    @patch("mpaws.init")
    @patch.dict(
        "os.environ",
        {"MPAWS_PROFILES": "profile1", "AWS_REGION": "eu-west-1"},
        clear=True,
    )
    def test_run_falls_back_to_aws_region(self, func_init, func_subprocess_run):

        mock_logger = unittest.mock.Mock()
        func_init.return_value = mock_logger
        func_subprocess_run.return_value = unittest.mock.Mock(
            stdout="", stderr="", returncode=0
        )

        with self.assertRaises(SystemExit):
            run(["ec2", "describe-instances"])

        _, kwargs = func_subprocess_run.call_args
        self.assertEqual(kwargs["env"]["AWS_REGION"], "eu-west-1")

    @patch("mpaws.subprocess.run")
    @patch("mpaws.init")
    @patch.dict(
        "os.environ",
        {"MPAWS_PROFILES": "profile1", "MPAWS_REGIONS": "us-east-1"},
        clear=True,
    )
    def test_run_prints_stdout_on_success(self, func_init, func_subprocess_run):

        mock_logger = unittest.mock.Mock()
        func_init.return_value = mock_logger
        func_subprocess_run.return_value = unittest.mock.Mock(
            stdout="instance output", stderr="", returncode=0
        )

        with self.assertRaises(SystemExit) as context:
            run(["ec2", "describe-instances"])

        self.assertEqual(context.exception.code, 0)
        mock_logger.info.assert_any_call("Standard output:")

    @patch("mpaws.subprocess.run")
    @patch("mpaws.init")
    @patch.dict(
        "os.environ",
        {"MPAWS_PROFILES": "profile1", "MPAWS_REGIONS": "us-east-1"},
        clear=True,
    )
    def test_run_counts_error_and_prints_stderr(self, func_init, func_subprocess_run):

        mock_logger = unittest.mock.Mock()
        func_init.return_value = mock_logger
        func_subprocess_run.return_value = unittest.mock.Mock(
            stdout="", stderr="boom", returncode=1
        )

        with self.assertRaises(SystemExit) as context:
            run(["ec2", "describe-instances"])

        self.assertEqual(context.exception.code, 1)
        mock_logger.error.assert_any_call("Standard error:")

    @patch("mpaws.subprocess.run")
    @patch("mpaws.init")
    @patch.dict(
        "os.environ",
        {"MPAWS_PROFILES": "profile1", "MPAWS_REGIONS": "us-east-1"},
        clear=True,
    )
    def test_run_counts_error_on_exception(self, func_init, func_subprocess_run):

        mock_logger = unittest.mock.Mock()
        func_init.return_value = mock_logger
        func_subprocess_run.side_effect = OSError("command not found")

        with self.assertRaises(SystemExit) as context:
            run(["ec2", "describe-instances"])

        self.assertEqual(context.exception.code, 1)
        mock_logger.error.assert_any_call("An exception occurred: command not found")

    @patch("mpaws.subprocess.run")
    @patch("mpaws.init")
    @patch.dict(
        "os.environ",
        {
            "MPAWS_PROFILES": "profile1,profile2",
            "MPAWS_REGIONS": "us-east-1,ap-southeast-2",
        },
        clear=True,
    )
    def test_run_executes_once_per_profile_and_region_permutation(
        self, func_init, func_subprocess_run
    ):

        mock_logger = unittest.mock.Mock()
        func_init.return_value = mock_logger
        func_subprocess_run.return_value = unittest.mock.Mock(
            stdout="", stderr="", returncode=0
        )

        with self.assertRaises(SystemExit) as context:
            run(["ec2", "describe-instances"])

        self.assertEqual(context.exception.code, 0)
        self.assertEqual(func_subprocess_run.call_count, 4)

    def test_cli_help_shows_usage(self):

        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output

    @patch("importlib.metadata.version")
    def test_cli_version_shows_version_info(self, func_version):

        func_version.return_value = "1.2.3"

        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "mpaws, version 1.2.3" in result.output

        func_version.assert_called_once_with("mpaws")

    @patch("mpaws.run")
    def test_cli_forwards_args_to_run(self, func_run):

        func_run.return_value = None

        runner = CliRunner()
        runner.invoke(cli, ["ec2", "describe-instances"])

        func_run.assert_called_once_with(["ec2", "describe-instances"])

    @patch("mpaws.run")
    def test_cli_forwards_unknown_flags_to_run(self, func_run):

        func_run.return_value = None

        runner = CliRunner()
        runner.invoke(cli, ["ec2", "describe-instances", "--query", "foo"])

        func_run.assert_called_once_with(
            ["ec2", "describe-instances", "--query", "foo"]
        )

    @patch("mpaws.run")
    def test_cli_forwards_underscore_shell_command_to_run(self, func_run):

        func_run.return_value = None

        runner = CliRunner()
        runner.invoke(cli, ["_", "echo", "hello"])

        func_run.assert_called_once_with(["_", "echo", "hello"])
