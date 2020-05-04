import pytest

from .deps import *

@pytest.fixture
def std():
    obj = Internals()
    src = """use std"""

    program = obj.compiler.compile(src)
    obj.interpreter.load(program)
    return obj

class TestStdlib(Test):
    def test_random(self, std):
        ret = std.interpreter.call('random', [])
        self.assertIsInstance(ret, Number)
        self.assertTrue(0 <= float(ret) <= 1)

    def test_sqrt(self, std):
        ret = std.interpreter.call('sqrt', [16])
        self.assertEqual(4, float(ret))
