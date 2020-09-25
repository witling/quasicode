import pytest

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
        self.assertIsInstance(ret, list)
        self.assertEqual(0, len(ret))

        ret = internals.interpreter.call('create_indirect')
        self.assertIsInstance(ret, list)
        self.assertEqual(0, len(ret))

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
        self.assertIsInstance(ret, list)
        self.assertTrue(ret)

        for i in range(4):
            self.assertEqual(i+1, float(ret[i]))

    def test_creation_inline(self, internals):
        src = """
und zwar create_indirect
    (liste mit 1 2 3) und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('create_indirect')
        self.assertIsInstance(ret, list)

        for i in range(3):
            self.assertEqual(i+1, float(ret[i]))

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
        self.assertIsInstance(ret, list)
        self.assertEqual(4, len(ret))

        for expect, got in zip([2, 4, 5, 3], map(int, ret)):
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

    def test_slice_full(self, internals):
        src = """
und zwar create
    eingabe ist liste mit 1 2 3 4
    (eingabe von 1 bis 4) und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('create')
        self.assertEqual(3, len(ret))

        for expected, got in zip([1, 2, 3], map(int, ret)):
            self.assertEqual(expected, got)

    def test_slice_till(self, internals):
        src = """
und zwar create
    eingabe ist liste mit 1 2 3 4
    (eingabe bis 2) und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('create')
        self.assertEqual(1, len(ret))
        self.assertEqual(1, int(ret[0]))

    def test_slice_from(self, internals):
        src = """
und zwar create
    eingabe ist liste mit 1 2 3 4
    (eingabe von 2) und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('create')
        self.assertEqual(3, len(ret))

        for expected, got in zip([2, 3, 4], map(int, ret)):
            self.assertEqual(expected, got)

    def test_liste_lib(self, internals):
        src = """use liste
ls ist liste mit 1 2 3 4
        """
        program = internals.compiler.compile(src, auto_main=True)
        internals.interpreter.load(program)
        internals.interpreter.run()

        ret = internals.interpreter.call('länge', Expr.var('ls'))
        self.assertEqual(4, ret)

        internals.interpreter.call('lösche', Expr.var('ls'), 1)

        ret = internals.interpreter.call('länge', Expr.var('ls'))
        self.assertEqual(3, ret)

        pop_front = internals.interpreter.call('pop_front', Expr.var('ls'))
        self.assertEqual(2, pop_front)
        pop_back = internals.interpreter.call('pop', Expr.var('ls'))
        self.assertEqual(4, pop_back)

        internals.interpreter.call('push', Expr.var('ls'), 3)
        ctx = internals.interpreter._vm.ctx()
        self.assertEqual([3, 3], ctx.globals('ls'))
