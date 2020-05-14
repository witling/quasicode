import pytest

from .deps import *

class TestStdlib(Test):
    def test_random(self, internals):
        import io
        stdin = io.StringIO('hej\n')
        internals.interpreter._ctx.set_stdin(stdin)
        ret = internals.interpreter.call('bitte?', ['was war die frage?'])

        self.assertEqual('hej', ret)

    def test_sqrt(self, internals):
        internals.interpreter.call('quasi', ['hi'])
