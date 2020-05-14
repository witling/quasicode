import unittest

from .deps import *

class TestLists(Test):
    def test_creation(self, internals):
        src = """
und zwar create_indirect
    obj1 ist liste
    obj1 und fertig

und zwar create
    liste und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('create')
        self.assertIsInstance(ret, Liste)

        ret = internals.interpreter.call('create_indirect')
        self.assertIsInstance(ret, Liste)

    def test_creation_parameterized(self, internals):
        src = """
und zwar create_indirect
    a ist 1
    b ist 3
    obj1 ist liste mit a 2 b 4
    obj1 und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('create_indirect')
        self.assertIsInstance(ret, Liste)
        self.assertTrue(ret._val)

        for i in range(4):
            self.assertEqual(i+1, float(ret._val[i]))

    def test_creation_inline(self, internals):
        src = """
und zwar create_indirect
    (liste mit 1 2 3) und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('create_indirect')
        self.assertIsInstance(ret, Liste)

        for i in range(3):
            self.assertEqual(i+1, float(ret._val[i]))

    def test_set_index(self, internals):
        src = """
und zwar create_indirect
    eingabe ist liste mit 3 4 5 1
    eingabe bei 1 ist 2
    eingabe bei 4 ist 3
    eingabe und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('create_indirect')
        self.assertIsInstance(ret, Liste)

        for expect, got in zip([2, 4, 5, 3], map(int, ret._val)):
            self.assertEqual(expect, got)

    def test_get_index(self, internals):
        src = """
und zwar first
    eingabe ist liste mit 3 4 5 1
    (eingabe bei 1) und fertig
"""

        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('first')
        self.assertEqual(3, int(ret))
