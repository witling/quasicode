import unittest

from ast import *
from parser import Parser

def parse(src):
    parser = Parser()
    return parser.parse(src)

class TestParsing(unittest.TestCase):
    def test_declare(self):
        src = """
und zwar hier action please
    quasi 1
        """
        program = parse(src)

        self.assertIsInstance(program[0], Declaration)
        self.assertTrue(program[0].is_main())

    def test_declare_args(self):
        src = """
und zwar hier mit a b
    quasi 1
        """
        program = parse(src)

        self.assertIsInstance(program[0], Declaration)
        self.assertEqual(len(program[0].args()), 2)

    def test_declare_args_main(self):
        src = """
und zwar hier mit a b action please
    quasi 1
        """
        program = parse(src)

        self.assertIsInstance(program[0], Declaration)
        self.assertEqual(len(program[0].args()), 2)
        self.assertTrue(program[0].is_main())
