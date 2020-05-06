import pytest

from .deps import *

@pytest.fixture(scope='session')
def srcdir(tmpdir_factory):
    d = tmpdir_factory.mktemp('tmp')

    fname = d.join('test.qc')
    src = """
und zwar gib_aus
    quasi "hallo welt"
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
