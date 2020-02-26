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

    def test_branch(self):
        src = """
kris? 1 das ist 1
    quasi "lol"
        """
        program = parse(src)
        self.assertIsInstance(program[0], If)

    def test_branch_elif(self):
        src = """
kris? 3 das ist 1
    quasi "fizz"
kris?? 3 das ist 2
    quasi "buzz"
kris?? 3 das ist 3
    quasi "buzz"
        """
        program = parse(src)
        self.assertIsInstance(program[0], If)
        self.assertEqual(len(program[0].branches()), 3)

    def test_branch_elif_else(self):
        src = """
kris? 1 das ist 2
    quasi "fizz"
kris?? 1 das ist 1
    quasi "buzz"
ach kris.
    quasi "nix"
        """
        program = parse(src)
        self.assertIsInstance(program[0], If)
        self.assertEqual(len(program[0].branches()), 3)
