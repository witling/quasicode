import pytest

from .deps import *

class TestStdlib(Test):
    def test_random(self, internals):
        import io
        stdin = io.StringIO('hej\n')
        internals.interpreter._ctx.set_stdin(stdin)
        ret = internals.interpreter.call('bitte?', 'was war die frage?')

        self.assertEqual('hej', str(ret))

    def test_sqrt(self, internals):
        internals.interpreter.call('quasi', 'hi')

    def test_assert(self, internals):
        internals.interpreter.call('assert', True)

        with pytest.raises(AssertionError):
            internals.interpreter.call('assert', False)

#    def test_json_dumps(self, internals):
#        src = """
#use json
#
#d ist menge
#d.x ist 1
#d.y ist 2
#"""
#        program = internals.compiler.compile(src)
#        internals.interpreter.load(program)
#        internals.interpreter.run()
#
#        ret = internals.interpreter.call('dumps', Expr.var('d')).to_py()
#        self.assertEqual(0, len(ret))
