import unittest

from generate import Compiler
from interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self._compiler = Compiler()

    def test_maths(self):
        src = """
und zwar const
    42 und fertig

und zwar rechne mit x
    (x + 1) und fertig
        """
        program = self._compiler.compile(src)

        interpreter = Interpreter()
        interpreter.load(program)

        self.assertEqual(float(interpreter.call('const')), 42)
        self.assertEqual(float(interpreter.call('rechne', [1])), 2)
