# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import os
import unittest
import pytest
from mpaws import run

class TestInit(unittest.TestCase):

    def setUp(self):
        os.unsetenv('MPAWS_PROFILES')
        if 'MPAWS_PROFILES' in os.environ:
            os.environ.pop('MPAWS_PROFILES')
        os.unsetenv('MPAWS_REGIONS')
        if 'MPAWS_REGIONS' in os.environ:
            os.environ.pop('MPAWS_REGIONS')
        os.unsetenv('AWS_DEFAULT_REGION')
        if 'AWS_DEFAULT_REGION' in os.environ:
            os.environ.pop('AWS_DEFAULT_REGION')
        os.unsetenv('AWS_REGION')
        if 'AWS_REGION' in os.environ:
            os.environ.pop('AWS_REGION')

    def test_run_with_help_arg_and_no_mpaws_profiles_no_mpaws_regions(self):
        with pytest.raises(SystemExit) as e:
            run('ec2 describe-instances')
            assert e.type == SystemExit
            assert e.value.code == 0
