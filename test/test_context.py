import pytest

from .deps import *

class TestContext(Test):
    def test_restricted_allowed(self):
        src = """use std
use net
"""
        compiler = Compiler()
        interpreter = Interpreter(restricted=True)
        interpreter._ctx.set_allowed_modules(['std'])

        program = compiler.compile(src)
        interpreter.load(program)

        with pytest.raises(ImportError):
            interpreter.run()

    def test_restricted_blocked(self):
        src = """use std
use net
"""
        compiler = Compiler()
        interpreter = Interpreter(restricted=True)
        interpreter._ctx.set_blocked_modules(['net'])

        program = compiler.compile(src)
        interpreter.load(program)

        with pytest.raises(ImportError):
            interpreter.run()

    def test_restricted_allowed_all(self):
        src = """use std
use net
"""
        compiler = Compiler()
        interpreter = Interpreter(restricted=True)
        interpreter._ctx.set_allowed_modules(['std', 'net'])

        program = compiler.compile(src)
        interpreter.load(program)
        interpreter.run()

        self.assertEqual(0, interpreter._ctx.exit_code())
