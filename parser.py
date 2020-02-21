from ast import *
from more_itertools import peekable
from syntax import *

import re

class Indent:
    def __init__(self, depth=0):
        self._depth = int(depth)

    def depth(self):
        return self._depth

class Newline:
    pass

class Error(Exception):
    pass

class Lexer:
    INDENT_RE = re.compile('^(\\t|\s{4})+')
    INDENT_WIDTH = 4

    def lex(self, line: str):
        lexed = []
        match = self.INDENT_RE.match(line)
        if match:
            depth = match.span()[1]
            lexed.append(Indent(depth / self.INDENT_WIDTH))

        it = (part.lower() for part in line.strip().split(' ') if part != '')
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
        self._chain = []

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
                    cls = self._parse_keyword(line)
                    self._chain.append(cls())

                elif isinstance(token, Value):
                    value = next(line)
                    self._chain.append(value)
                    try:
                        cls = self._parse_keyword(line)
                        self._chain.append(cls())
                    except Error:
                        print('we have error, sir')
                else:
                    token = next(line)
                    self._chain.append(token)
        except StopIteration:
            pass

    def parse(self, content: str) -> list:
        lexed = (self._lexer.lex(line) for line in content.split('\n'))

        for line in lexed:
            self._parse_line(peekable(line))
            self._chain.append(Newline())

        reducer = Reducer(self._chain)
        return reducer.start()

class Reducer:
    def __init__(self, chain):
        self._it = peekable(chain)

    def _collect_block(self, min_depth=1):
        block = Block()
        while True:
            peek = self._it.peek()
            if not isinstance(peek, Indent) or not min_depth <= peek.depth():
                break

            if min_depth < peek.depth():
                sub = self._collect_block(min_depth + 1)
                block.append(sub)
            else:
                next(self._it)
                while True:
                    take = next(self._it)
                    block.append(take)
                    if isinstance(take, Newline):
                        break
        return block

    def _strip_block(self, block):
        stripped = []
        for s in block:
            if isinstance(s, Newline) or isinstance(s, Indent):
                continue
            if isinstance(s, Block):
                stripped.append(self._strip_block(s))
            else:
                stripped.append(s)
        return stripped

    def _sub_reduce(self, it):
        stack, done = [], []

        for token in it:
            if isinstance(token, Declaration):
                stack.append(token)
            elif isinstance(token, Value):
                if stack:
                    top = stack[-1]
                    if isinstance(top, Declaration):
                        assert isinstance(token, Ident)
                        top.set_name(token)
                else:
                    stack.append(token)
            elif isinstance(token, MainMarker):
                assert stack
                stack[-1].add_marker(token)
            elif isinstance(token, Newline):
                if stack:
                    top = stack[-1]
                    if isinstance(top, NestedStatement):
                        block = self._collect_block()
                        block = self._sub_reduce(iter(block))
                        block = self._strip_block(block)
                        top.set_block(block)
                    done.append(stack.pop())
            else:
                done.append(token)

        return done

    def start(self):
        return self._sub_reduce(self._it)
