from ast import *
from program import Program
from syntax import *

class Error(Exception):
    pass

class Lexer:
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

    def _peek_is(self, it, other):
        peek = it.peek()
        return type(peek) == type(other) and peek.eq(other)

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
                    print(item)

                elif isinstance(token, Value):
                    next(line)
        except StopIteration:
            pass

    def parse(self, content: str) -> Program:
        from more_itertools import peekable

        lexed = (self._lexer.lex(line) for line in content.split('\n'))

        for line in lexed:
            self._parse_line(peekable(line))

        return self._program
