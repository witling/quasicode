import pytest

from .deps import *

class TestParsing(Test):
    def test_declare(self, internals):
        src = """
und zwar hier action please
    quasi 1
        """
        program = internals.parser.parse(src)

        self.assertIsInstance(program[0], Declaration)
        self.assertTrue(program[0].is_main())

    def test_declare_args(self, internals):
        src = """
und zwar hier mit a b
    quasi 1
        """
        program = internals.parser.parse(src)

        self.assertIsInstance(program[0], Declaration)
        self.assertEqual(2, len(program[0].args()))

    def test_declare_args_main(self, internals):
        src = """
und zwar hier mit a b action please
    quasi 1
        """
        program = internals.parser.parse(src)

        self.assertIsInstance(program[0], Declaration)
        self.assertEqual(2, len(program[0].args()))
        self.assertTrue(program[0].is_main())

    def test_branch(self, internals):
        src = """
kris? 1 das ist 1
    quasi "lol"
        """
        program = internals.parser.parse(src)
        self.assertIsInstance(program[0], If)

    def test_branch_elif(self, internals):
        src = """
kris? 3 das ist 1
    quasi "fizz"
kris?? 3 das ist 2
    quasi "buzz"
kris?? 3 das ist 3
    quasi "buzz"
        """
        program = internals.parser.parse(src)
        self.assertIsInstance(program[0], If)
        self.assertEqual(3, len(program[0].branches()))

    def test_branch_elif_else(self, internals):
        src = """
kris? 1 das ist 2
    quasi "fizz"
kris?? 1 das ist 1
    quasi "buzz"
ach kris.
    quasi "nix"
        """
        program = internals.parser.parse(src)
        self.assertIsInstance(program[0], If)
        self.assertEqual(3, len(program[0].branches()))

    def test_repeat(self, internals):
        src = """
0 also i
das holen wir nach
    i ist i + 1
    kris? i das ist 10
        patrick!
        """
        program = internals.parser.parse(src)
        self.assertIsInstance(program[0], Assign)
        self.assertIsInstance(program[1], Repeat)

    def test_string_parsing(self, internals):
        src = """
"hello world" also str1
str2 ist 'hallo welt'
        """
        program = internals.parser.parse(src)
        self.assertIsInstance(program[0], RHAssign)
        self.assertIsInstance(program[1], LHAssign)

    def test_parens(self, internals):
        src = """
i ist (0 + 1)
        """
        program = internals.parser.parse(src)
        self.assertIsInstance(program[0], LHAssign)
