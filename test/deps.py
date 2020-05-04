from os.path import abspath, dirname, join
import pytest
import sys

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from qclib import *

class Test:
    def assertIsInstance(self, obj, cls):
        self.assertTrue(isinstance(obj, cls))

    def assertEqual(self, expected, got):
        self.assertTrue(expected == got)

    def assertFalse(self, expr):
        self.assertTrue(not expr)

    def assertTrue(self, expr):
        assert expr

class Internals:
    def __init__(self):
        self.interpreter = Interpreter()
        self.compiler = Compiler()
        self.parser = self.compiler.parser()

@pytest.fixture
def internals():
    return Internals()
