import unittest

from .deps import *

class TestObjects(Test):
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
