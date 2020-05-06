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
