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
        self.assertTrue(self._program.save(self._fname))

    def test_2loading(self):
        loaded_prog = Program.load(self._fname)
        self.assertIsInstance(loaded_prog, Program)
