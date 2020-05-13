import pytest

from .deps import *

class TestStdlib(Test):
    def test_random(self, internals):
        ret = internals.interpreter.call('random', [])
        self.assertIsInstance(ret, Number)
        self.assertTrue(0 <= float(ret) <= 1)

    def test_sqrt(self, internals):
        ret = internals.interpreter.call('sqrt', [16])
        self.assertEqual(4, float(ret))
