import pytest

from .deps import *

class TestContext(Test):
    def test_restricted(self, internals):
        src = """use std
use net
        """
        interpreter = Interpreter(restricted=True)
        interpreter._ctx.set_allowed_modules(['std'])

        program = internals.compiler.compile(src)

        with pytest.raises(Exception):
            interpreter.load(program)
