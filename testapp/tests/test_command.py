from datetime import datetime
from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class Test(TestCase):
    def test_normal(self):
        out = StringIO()
        err = StringIO()
        call_command('some_command', stdout=out, stderr=err)
        self.assertEqual(out.getvalue(), 'info message\n')
        self.assertEqual(err.getvalue(), 'error message\nexception handled\n')
    
    def test_max_verbosity(self):
        out = StringIO()
        err = StringIO()
        call_command('some_command', verbosity=3, stdout=out, stderr=err)
        self.assertEqual(out.getvalue(), 'info message\ndebug message\n')
        self.assertEqual(err.getvalue(), 'error message\nexception handled\n')

    def test_silent(self):
        # TODO: same output as v=1 - maybe use it differently?
        out = StringIO()
        err = StringIO()
        call_command('some_command', verbosity=0, stdout=out, stderr=err)
        self.assertEqual(out.getvalue(), 'info message\n')
        self.assertEqual(err.getvalue(), 'error message\nexception handled\n')
