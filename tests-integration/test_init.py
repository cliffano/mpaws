# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import os
import unittest
from mpaws import run

class TestInit(unittest.TestCase):

    def setUp(self):
        os.unsetenv('MPAWS_PROFILES')
        if 'MPAWS_PROFILES' in os.environ:
            os.environ.pop('MPAWS_PROFILES')

    def test_run_with_help_arg_and_no_mpaws_profiles(self):
        run('help')
