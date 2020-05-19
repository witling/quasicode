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

    def test_auto_main(self, internals):
        src = """
quasi "toplevel"
"""
        program = internals.compiler.compile(src, auto_main=True)
        self.assertTrue('__main__' in program.idents())

        import io
        stdout = io.StringIO()
        internals.interpreter._ctx.set_stdout(stdout)

        internals.interpreter.load(program)
        internals.interpreter.run()

        self.assertEqual('toplevel\n', stdout.getvalue())

    def test_misinterpreted_return(self, internals):
        src = '''
und zwar main action please
    4 im quadrat und fertig
        '''

        program = internals.compiler.compile(src)
        first_stmt = program['main'].block()[0]

        self.assertEqual(Return, first_stmt.__class__)

    def test_constant_declaration(self, internals):
        src = '''
pi ist 3
2 also e
        '''

        program = internals.compiler.compile(src)

        self.assertEqual(3, int(program['pi']))
        self.assertEqual(2, int(program['e']))
