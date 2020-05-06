import pytest

from .deps import *

class TestInterpreter(Test):
    def test_maths(self, internals):
        src = """
und zwar const
    42 und fertig

und zwar rechne mit x
    (x + 1) und fertig
        """
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        self.assertEqual(42, float(internals.interpreter.call('const')))
        self.assertEqual(2, float(internals.interpreter.call('rechne', [1])))

    def test_logical(self, internals):
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
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        self.assertTrue(internals.interpreter.call('or_wahr'))
        self.assertFalse(internals.interpreter.call('or_falsch'))

        self.assertTrue(internals.interpreter.call('and_wahr'))
        self.assertFalse(internals.interpreter.call('and_falsch'))

    def test_comparison(self, internals):
        src = """
und zwar kleiner mit a b
    kris? a < b
        uzbl und fertig
    (not uzbl) und fertig
        """
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        self.assertTrue(internals.interpreter.call('kleiner', [1, 2]))
        self.assertFalse(internals.interpreter.call('kleiner', [2, 1]))
        self.assertFalse(internals.interpreter.call('kleiner', [2, 2]))

    def test_unknown_use(self, internals):
        src = """use non_existent"""
        program = internals.compiler.compile(src)
        with pytest.raises(LookupException):
            internals.interpreter.load(program)
