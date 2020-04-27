import pytest

from .deps import *

class TestConstants(Test):
    def test_uzbl(self, internals):
        src = """
und zwar teste
    a ist uzbl
    b ist (not uzbl)
    kris? a das ist b
        1 und fertig
    0 und fertig
        """
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('teste', [])
        self.assertIsInstance(ret, Number)
        self.assertEqual(float(0), float(ret))
