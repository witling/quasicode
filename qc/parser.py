from ast import *
from more_itertools import peekable
from syntax import *

import re

class Indent:
    def __init__(self, depth=0):
        self._depth = int(depth)

    def depth(self):
        return self._depth

    def __str__(self):
        return '\\t'

class Newline:
    def __str__(self):
        return '\\n'

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
                lexed.append(Number(float(lexem)))
            else:
                lexed.append(Ident(lexem))

        return lexed

class Parser:
    def __init__(self):
        self._lexer = Lexer()
        self._chain = []

    def _take_while_keyword(self, it):
        stc = Block()
        try:
            while isof(it.peek(), Keyword):
                stc.append(next(it))
        except StopIteration:
            pass
        return stc

    def _keywords_to_ast(self, stc):
        it = iter(stc)
        node = SYN_TREE[next(it).name()]
        name = None

        for k in it:
            try:
                name = k.name()
                node = node[name]
            except KeyError:
                possible = ','.join(map(lambda x: '`{}`'.format(x), node.keys()))
                raise Error('expected one of {}. got `{}`'.format(possible, name))

        if '_op' not in node:
            raise Error('unexpected symbol `{}` in `{}`'.format(name, stc))

        return node['_op']
    
    def _parse_keyword(self, it):
        stc = self._take_while_keyword(it)
        return self._keywords_to_ast(stc)

    def _parse_line(self, line):
        try:
            while True:
                token = line.peek()
                if isof(token, Keyword):
                    cls = self._parse_keyword(line)
                    self._chain.append(cls())

                elif isof(token, Value):
                    self._chain.append(next(line))

                else:
                    self._chain.append(next(line))
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

    def _collect_till_newline(self, it=None):
        it = it if it else self._it
        block = []
        while True:
            take = next(it)
            block.append(take)
            if isof(take, Newline):
                break
        return block

    def _collect_block(self, it=None, min_depth=1):
        it = it if it else self._it
        block = Block()
        try:
            while True:
                peek = it.peek()
                if isof(peek, Block):
                    block = next(it)
                    break

                if not isof(peek, Indent) or not min_depth <= peek.depth():
                    break

                if min_depth < peek.depth():
                    sub = self._collect_block(it = it, min_depth = min_depth + 1)
                    block.append(sub)
                else:
                    next(it)
                    block.extend(self._collect_till_newline(it))
        except StopIteration:
            pass
        return block

    def _strip_block(self, block):
        stripped = Block()
        for s in block:
            if isof(s, Newline) or isof(s, Indent):
                continue
            if isof(s, Block):
                stripped.append(self._strip_block(s))
            else:
                stripped.append(s)
        return stripped

    def _sub_reduce(self, it):
        stack, done = [], []

        for token in it:
            #print(list(map(str, stack)), list(map(str, done)))
            #print(token)

            if isof(token, Declaration):
                stack.append(token)

            elif isof(token, Value):
                if stack:
                    top = stack[-1]
                    if isof(top, Declaration):
                        assert isof(token, Ident)
                        top.set_name(token)

                    elif isof(top, Branch):
                        condition = self._collect_till_newline(it)
                        block = self._collect_block(it)
                        top.add_branch(condition, block)

                    elif isof(top, Print) or isof(top, Operator):
                        top.add_arg(token)
                else:
                    stack.append(token)

            #elif isof(token, Block):
            #    block = self._sub_reduce(peekable(token))
            #    block = self._strip_block(block)
            #    #top = stack[-1]

            elif isof(token, MainMarker):
                assert stack
                stack[-1].add_marker(token)

            elif isof(token, Newline):
                if stack:
                    top = stack[-1]
                    if isof(top, NestedStatement):
                        block = self._collect_block(it)
                        block = self._sub_reduce(peekable(block))
                        block = self._strip_block(block)
                        top.set_block(block)
                    elif isof(top, Print):
                        pass
                    else:
                        continue

                    done.append(stack.pop())

            elif isof(token, Assign):
                last = stack.pop()

                rest = self._collect_till_newline(it)
                rest = self._sub_reduce(peekable(rest))
                rest = self._strip_block(rest)

                if isof(token, LHAssign):
                    token.set_ident(last)
                    token.set_value(rest)
                else:
                    token.set_ident(rest)
                    token.set_value(last)

                done.append(token)

            elif isof(token, Operator):
                if stack:
                    top = stack.pop()
                    if not (isof(top, Value) or isof(top, Operator)):
                        print(type(top))
                        assert False
                    token.add_arg(top)
                    stack.append(token)
                else:
                    raise Error('prefix operators not supported')

            elif isof(token, Branch):
                if stack:
                    top = stack[-1]
                    if isof(top, If) and isof(token, If):
                        done.append(stack.pop())
                else:
                    assert isof(token, If)

                if isof(token, Elif):
                    token = stack.pop()

                condition = self._collect_till_newline(it)
                condition = self._sub_reduce(peekable(condition))
                condition = self._strip_block(condition)
                block = self._collect_block(it)
                block = self._sub_reduce(peekable(block))
                block = self._strip_block(block)

                token.add_branch(condition, block)

                stack.append(token)

            elif isof(token, Print) or isof(token, Repeat):
                stack.append(token)

            else:
                done.append(token)

        done.extend(stack)

        return done

    def start(self):
        return self._sub_reduce(self._it)
