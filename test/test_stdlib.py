import unittest

from deps import *

class TestStdlib(unittest.TestCase):
    def setUp(self):
        self._interpreter = Interpreter()

        src = """use std"""
        program = Compiler().compile(src)
        self._interpreter.load(program)

    def test_random(self):
        ret = self._interpreter.call('random', [])
        self.assertIsInstance(ret, Number)
        self.assertTrue(0 <= float(ret) <= 1)

    def test_sqrt(self):
        ret = self._interpreter.call('sqrt', [16])
        self.assertEqual(float(ret), 4)
