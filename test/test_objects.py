import unittest

from .deps import *

class TestObjects(Test):
    def test_creation(self, internals):
        src = """
und zwar create_indirect
    obj1 ist menge
    obj1 und fertig

und zwar create
    menge und fertig
        """
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('create')
        self.assertIsInstance(ret, Menge)

        ret = internals.interpreter.call('create_indirect')
        self.assertIsInstance(ret, Menge)

    def test_object_access(self, internals):
        src = """
und zwar return
    obj1 ist menge
    obj1.b ist 1

    obj1.sub ist menge
    obj1.sub.a ist 2

    obj1 und fertig
        """
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('return')
        self.assertEqual(1, float(ret['b']))
        self.assertEqual(2, float(ret['sub']['a']))
