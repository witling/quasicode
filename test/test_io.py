import io
import pytest

from .deps import *

class TestIO(Test):
    def test_reading_stdin(self, internals):
        src = """
und zwar getname
    mein_name ist (bitte? "wie ist dein name? ")
    quasi mein_name
        """
        sin, sout = io.StringIO('alfred\n'), io.StringIO()
        internals.interpreter._ctx.set_stdin(sin)
        internals.interpreter._ctx.set_stdout(sout)
        internals.interpreter._ctx.disable_funny_mode()

        program = internals.compiler.compile(src)
        internals.interpreter.load(program)
        internals.interpreter.call('getname')

        output = sout.getvalue()
        self.assertEqual('wie ist dein name? alfred\n\n', output)
