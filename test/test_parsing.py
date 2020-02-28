import unittest

from deps import *

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

    def test_repeat(self):
        src = """
0 also i
das holen wir nach
    i ist i + 1
    kris? i das ist 10
        patrick!
        """
        program = parse(src)
        self.assertIsInstance(program[0], Assign)
        self.assertIsInstance(program[1], Repeat)

    def test_string_parsing(self):
        src = """
"hello world" also str1
str2 ist 'hallo welt'
        """
        program = parse(src)
        self.assertIsInstance(program[0], RHAssign)
        self.assertIsInstance(program[1], LHAssign)

    def test_parens(self):
        src = """
i ist (0 + 1)
        """
        program = parse(src)
        self.assertIsInstance(program[0], LHAssign)
