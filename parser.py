from ast import *
from program import Program
from syntax import *

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

    def peek_is(self, it, other):
        peek = it.peek()
        return type(peek) == type(other) and peek.eq(other)

    def _parse_deep(self):
        pass

    def _parse_line(self, line):
        for token in line:
            if isinstance(token, Keyword):
                pass
            elif isinstance(token, Value):
                if token.is_assignable():
                    if self.peek_is(line, Keyword('ist')):
                        if self.peek_is(line, Keyword('also')):
                            pass
                    if self.peek_is(line, Keyword('also')):
                        if self.peek_is(line, Keyword('also')):
                            pass

    def parse(self, content: str) -> Program:
        from more_itertools import peekable

        lexed = (self._lexer.lex(line) for line in content.split('\n'))

        for line in lexed:
            self._parse_line(peekable(line))

        return self._program
