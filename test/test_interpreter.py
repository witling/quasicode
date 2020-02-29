import unittest

from deps import *

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self._compiler = Compiler()
        self._interpreter = Interpreter()

    def test_maths(self):
        src = """
und zwar const
    42 und fertig

und zwar rechne mit x
    (x + 1) und fertig
        """
        program = self._compiler.compile(src)
        self._interpreter.load(program)

        self.assertEqual(42, float(self._interpreter.call('const')))
        self.assertEqual(2, float(self._interpreter.call('rechne', [1])))

    def test_logical(self):
        src = """
und zwar or_wahr
    ((not uzbl) oder uzbl) und fertig

und zwar or_falsch
    ((not uzbl) oder (not uzbl)) und fertig

und zwar and_wahr
    (uzbl und uzbl) und fertig

und zwar and_falsch
    ((not uzbl) und uzbl) und fertig
        """
        program = self._compiler.compile(src)
        self._interpreter.load(program)

        self.assertTrue(self._interpreter.call('or_wahr'))
        self.assertFalse(self._interpreter.call('or_falsch'))

        self.assertTrue(self._interpreter.call('and_wahr'))
        self.assertFalse(self._interpreter.call('and_falsch'))
