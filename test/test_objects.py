import unittest

from deps import *

class TestObjects(unittest.TestCase):
    def setUp(self):
        self._compiler = Compiler()
        self._interpreter = Interpreter()

    def test_creation(self):
        src = """
        obj1 ist menge

        obj2.x ist 1
        obj2.y ist 1
        """
        program = self._compiler.compile(src)
        self._interpreter.load(program)
