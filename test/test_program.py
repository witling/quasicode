import unittest

from deps import *

class TestProgram(unittest.TestCase):
    def setUp(self):
        src = """
und zwar gib_aus
    quasi "hallo welt"
        """
        compiler = Compiler()
        self._program = compiler.compile(src)
        self._fname = '/tmp/qc_test_program.qcc'

    def test_1saving(self):
        with open(self._fname, 'wb') as f:
            self.assertTrue(self._program.save(f))

    def test_2loading(self):
        with open(self._fname, 'rb') as f:
            loaded_prog = Program.load(f)
            self.assertIsInstance(loaded_prog, Program)
