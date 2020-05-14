import pytest

from .deps import *

def node(ast, name):
    ls = list(ast.find_data(name))
    if not len(ls) == 1:
        return None
    return ls[0]

class TestParsing(Test):
    def test_declare(self, internals):
        src = """
und zwar hier action please
    quasi 1
"""
        ast = internals.parser.parse(src)

        self.assertTrue(node(ast, 'declare'))
        self.assertTrue(node(ast, 'marker_main'))

    def test_declare_args(self, internals):
        src = """
und zwar hier mit a b
    quasi 1
"""
        ast = internals.parser.parse(src)

        self.assertTrue(node(ast, 'declare'))

        args = node(ast, 'declare_args')
        self.assertTrue(args)
        self.assertEqual(2, len(args.children))

    def test_declare_args_main(self, internals):
        src = """
und zwar hier mit a b c action please
    quasi 1
"""
        ast = internals.parser.parse(src)

        self.assertTrue(node(ast, 'declare'))
        self.assertTrue(node(ast, 'marker_main'))

        args = node(ast, 'declare_args')
        self.assertTrue(args)
        self.assertEqual(3, len(args.children))

    def test_branch(self, internals):
        src = """
kris? 1 das ist 1
    quasi "lol"
"""
        ast = internals.parser.parse(src)

        branch = node(ast, 'if_branch')
        self.assertTrue(branch)
        self.assertEqual(2, len(branch.children))

    def test_branch_elif(self, internals):
        src = """
kris? 3 das ist 1
    quasi "fizz"
kris?? 3 das ist 2
    quasi "buzz"
kris?? 3 das ist 3
    quasi "buzz"
"""
        ast = internals.parser.parse(src)

        branch = node(ast, 'if_branch')
        self.assertTrue(branch)
        self.assertEqual(4, len(branch.children))

        elif_branches = list(branch.find_data('elif_branch'))
        self.assertEqual(2, len(elif_branches))

    def test_branch_elif_else(self, internals):
        src = """
kris? 1 das ist 2
    quasi "fizz"
kris?? 1 das ist 1
    quasi "buzz"
ach kris.
    quasi "nix"
"""
        ast = internals.parser.parse(src)

        branch = node(ast, 'if_branch')
        self.assertTrue(branch)
        self.assertEqual(4, len(branch.children))

        elif_branches = list(branch.find_data('elif_branch'))
        self.assertEqual(1, len(elif_branches))

        else_branches = list(branch.find_data('else_branch'))
        self.assertEqual(1, len(else_branches))

    def test_repeat(self, internals):
        src = """
0 also i
das holen wir nach
    i ist i + 1
    kris? i das ist 10
        patrick!
"""
        ast = internals.parser.parse(src)

        loop = node(ast, 'loop')
        self.assertTrue(loop)
        self.assertEqual(1, len(loop.children))

    def test_string_parsing(self, internals):
        src = """
"hello world" also str1
str2 ist "hallo welt"
"""
        ast = internals.parser.parse(src)

        strings = list(ast.find_data('value'))
        self.assertEqual(2, len(strings))

    def test_parens(self, internals):
        src = """
i ist (0 + 1)
"""
        ast = internals.parser.parse(src)

        self.assertTrue(ast)

    def test_script_termination(self, internals):
        src = """
und zwar ich_bin_so_kuhl action please
    quasi "kuhler als du"
        """
        ast = internals.parser.parse(src)

        self.assertTrue(ast)
