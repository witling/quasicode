import os
from os.path import abspath, dirname, join
import pytest
import sys

sys.path.insert(0, abspath(join(dirname(__file__), '..')))

if 'PYLOVM2_DEV_LOCATION' in os.environ:
    sys.path.insert(1, os.environ['PYLOVM2_DEV_LOCATION'])

from qclib import *

def dump_test(src):
    with open('/tmp/testout.qc', 'w') as fout:
        fout.write(src)

class Test:
    def assertIsInstance(self, obj, cls):
        self.assertTrue(isinstance(obj, cls))

    def assertEqual(self, expected, got):
        if expected == got:
            return
        print('expected', expected, ', got', got)
        self.assertTrue(False)

    def assertFalse(self, expr):
        self.assertTrue(not expr)

    def assertTrue(self, expr):
        assert expr

class Internals:
    def __init__(self):
        self.interpreter = Interpreter()
        self.interpreter.disable_funny_mode()

        self.compiler = Compiler()
        self.parser = self.compiler.parser()

@pytest.fixture
def internals():
    return Internals()
