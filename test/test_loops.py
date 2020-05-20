import pytest

from .deps import *

class TestLoops(Test):
    def test_explicit_break(self, internals):
        src = """
und zwar loop
    i ist 0
    das holen wir nach
        kris? i das ist 5
            i und fertig
        i ist i + 1
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)
        ret = internals.interpreter.call('loop')

        self.assertEqual(5, int(ret))

    def test_until(self, internals):
        src = """
und zwar loop
    i ist 0
    das holen wir nach bis i das ist 5
        i ist i + 1
    i und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)
        ret = internals.interpreter.call('loop')

        self.assertEqual(5, int(ret))

    def test_while(self, internals):
        src = """
und zwar loop
    i ist 0
    das holen wir nach solange i < 5
        i ist i + 1
    i und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)
        ret = internals.interpreter.call('loop')

        self.assertEqual(5, int(ret))
