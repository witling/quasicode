import pytest

from .deps import *

class TestCompiler(Test):
    def test_unexpected_toplevel(self, internals):
        src = """
quasi "test"
        """
        with pytest.raises(CompilerError):
            program = internals.compiler.compile(src)

    def test_double_main(self, internals):
        src = """
und zwar main2 action please
    quasi "test"

und zwar main1 action please
    quasi "test"
        """
        with pytest.raises(CompilerError):
            program = internals.compiler.compile(src)
