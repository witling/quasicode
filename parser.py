from ast import *
from program import Program
from syntax import *

import re

class Indent:
    pass

class Newline:
    pass

class Error(Exception):
    pass

class Lexer:
    INDENT_RE = re.compile('^(\\t|\s{4})*')

    def lex(self, line: str):
        lexed = []
        it = (part.lower() for part in line.split(' ') if part != '')
        for lexem in it:
            # parse strings here
            if lexem[0] == '"':
                lexed.append(String(lexem))
            elif lexem in KEYWORDS:
                lexed.append(Keyword(lexem))
            elif lexem.isnumeric():
                lexed.append(Number(lexem))
            else:
                lexed.append(Ident(lexem))
        return lexed

class Parser:
    def __init__(self):
        self._lexer = Lexer()
        self._program = Program()
        self._chain = []
        self._declare = None

    def _take_while_keyword(self, it):
        stc = []
        try:
            while isinstance(it.peek(), Keyword):
                stc.append(next(it))
        except StopIteration:
            pass
        return stc

    def _keywords_to_ast(self, stc):
        it = iter(stc)
        node = SYN_TREE[next(it).name()]
        for k in it:
            node = node[k.name()]
        return node['_op']
    
    def _parse_keyword(self, it):
        stc = self._take_while_keyword(it)
        return self._keywords_to_ast(stc)

    def _parse_line(self, line):
        try:
            while True:
                token = line.peek()
                if isinstance(token, Keyword):
                    item = self._parse_keyword(line)
                    if isinstance(item, Declaration):
                        assert not self._declare
                    self._chain.append(item)

                elif isinstance(token, Value):
                    value = next(line)
                    self._chain.append(value)
                    try:
                        item = self._parse_keyword(line)
                        self._chain.append(item)
                    except Error:
                        pass
        except StopIteration:
            pass

    def _reduce(self):
        pass

    def parse(self, content: str) -> Program:
        from more_itertools import peekable

        lexed = (self._lexer.lex(line) for line in content.split('\n'))

        for line in lexed:
            self._parse_line(peekable(line))
            self._chain.append(Newline())

        self._reduce()

        return self._program
