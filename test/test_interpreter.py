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
        self.assertEqual(2, float(internals.interpreter.call('rechne', 1)))

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

        self.assertTrue(internals.interpreter.call('kleiner', 1, 2))
        self.assertFalse(internals.interpreter.call('kleiner', 2, 1))
        self.assertFalse(internals.interpreter.call('kleiner', 2, 2))

    def test_power(self, internals):
        src = """
und zwar pow
    (4 hoch 4) und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('pow')
        self.assertEqual(256, int(ret))

    def test_power_squared(self, internals):
        src = """
und zwar pow
    (2 im quadrat) und fertig
"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)

        ret = internals.interpreter.call('pow')
        self.assertEqual(4, int(ret))

    def test_unknown_use(self, internals):
        src = """use non_existent"""
        program = internals.compiler.compile(src)
        with pytest.raises(LookupException):
            internals.interpreter.load(program)

    def test_unknown_global(self, internals):
        src = """quasi x"""
        program = internals.compiler.compile(src, auto_main=True)
        internals.interpreter.load(program)
        ec = internals.interpreter.run()

        self.assertEqual(1, ec)
        self.assertEqual(LookupException, internals.interpreter._ctx.last_error.__class__)

    def test_exit_code_success(self, internals):
        src = """quasi 1"""
        program = internals.compiler.compile(src, auto_main=True)
        internals.interpreter.load(program)
        ec = internals.interpreter.run()

        self.assertEqual(0, ec)
        self.assertEqual(None, internals.interpreter._ctx.last_error)

    def test_exit_code_fail(self, internals):
        src = """"""
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)
        ec = internals.interpreter.run()

        self.assertEqual(1, ec)

    def test_name_shadowing(self, internals):
        src = """
und zwar put mit x
    quasi x

und zwar main action please
    x ist 42
    y ist 1
    put y
    quasi x
        """
        import io
        stdout = io.StringIO()

        program = internals.compiler.compile(src)
        internals.interpreter._ctx.set_stdout(stdout)
        internals.interpreter.load(program)
        internals.interpreter.run()

        self.assertEqual('1.0\n42.0\n', stdout.getvalue())

    def test_breaking_from_nested_loop(self, internals):
        src = """
und zwar factorial mit x
    i ist 1
    prod ist 1
    das holen wir nach
        prod ist prod * i
        kris? i das ist x
            prod und fertig
        i ist i + 1
        """
        program = internals.compiler.compile(src)
        internals.interpreter.load(program)
        ret = internals.interpreter.call('factorial', 3)

        self.assertEqual(6, int(ret))
        self.assertEqual([], internals.interpreter._ctx._loops)
