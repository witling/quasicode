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
        self.assertEqual(0, len(ret._val))

        ret = internals.interpreter.call('create_indirect')
        self.assertIsInstance(ret, Liste)
        self.assertEqual(0, len(ret._val))

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
        self.assertEqual(4, len(ret._val))

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

    def test_slice_full(self, internals):
        src = """
und zwar create
    eingabe ist liste mit 1 2 3 4
    (eingabe von 1 bis 4) und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('create')
        self.assertEqual(3, len(ret._val))

        for expected, got in zip([1, 2, 3], map(int, ret._val)):
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
        self.assertEqual(1, len(ret._val))
        self.assertEqual(1, int(ret._val[0]))

    def test_slice_from(self, internals):
        src = """
und zwar create
    eingabe ist liste mit 1 2 3 4
    (eingabe von 2) und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('create')
        self.assertEqual(3, len(ret._val))

        for expected, got in zip([2, 3, 4], map(int, ret._val)):
            self.assertEqual(expected, got)

    def test_liste_lib(self, internals):
        src = """use liste
ls ist liste mit 1 2 3 4
        """
        program = internals.compiler.compile(src, auto_main=True)
        internals.interpreter.load(program)
        internals.interpreter.run()

        ret = internals.interpreter.call('länge', Ident('ls'))
        self.assertEqual(4, int(ret))

        internals.interpreter.call('lösche', Ident('ls'), 1)

        ret = internals.interpreter.call('länge', Ident('ls'))
        self.assertEqual(3, int(ret))

        pop_front = internals.interpreter.call('pop_front', Ident('ls'))
        self.assertEqual(2, pop_front)
        pop_back = internals.interpreter.call('pop', Ident('ls'))
        self.assertEqual(4, pop_back)

        internals.interpreter.call('push', Ident('ls'), 3)
        ls = internals.interpreter._ctx['ls']
        self.assertEqual([3, 3], list(map(int, ls._val)))
