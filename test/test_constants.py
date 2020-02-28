import unittest

from deps import *

class TestConstants(unittest.TestCase):
    def setUp(self):
        self._interpreter = Interpreter()
        self._compiler = Compiler()

    def test_uzbl(self):
        src = """
und zwar teste
    a ist uzbl
    b ist (not uzbl)
    kris? a das ist b
        1 und fertig
    0 und fertig
        """
        program = self._compiler.compile(src)
        self._interpreter.load(program)

        ret = self._interpreter.call('teste', [])
        self.assertIsInstance(ret, Number)
        self.assertTrue(0, float(ret))
