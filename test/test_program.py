import pytest

from .deps import *

@pytest.fixture(scope='session')
def srcdir(tmpdir_factory):
    d = tmpdir_factory.mktemp('tmp')

    fname = d.join('test.qc')
    src = """
und zwar gib_aus
    quasi "hallo welt"

und zwar main action please
    oettinger
"""
    fname.write(src)

    return d

class TestProgram(Test):
    def test_saving(self, srcdir, internals):
        fname = srcdir.join('test.qc')
        with open(str(fname), 'r') as fp:
            src = fp.read()

        program = internals.compiler.compile(src)
        self.assertTrue(program.save('{}c'.format(fname)))

    def test_loading(self, srcdir):
        fname = srcdir.join('test.qcc')
        loaded_prog = Program.load(str(fname))
        self.assertIsInstance(loaded_prog, Program)
        self.assertTrue(loaded_prog._file.endswith('test.qcc'))
        self.assertEqual('test', loaded_prog.modname())

    def test_global_variables(self, internals):
        src = """
pi ist 3
ls ist liste mit 1 2 3
        """
        program = internals.compiler.compile(src)

        self.assertEqual(3, int(program['pi']))
        self.assertEqual([1, 2, 3], list(map(int, program['ls'])))
