from more_itertools import peekable
import re

from ..ast import *

from .error import ParserError
from .syntax import *

peek_is = lambda cls: lambda it: isof(it.peek(), cls)

def take_while(it, pred: callable):
    collect = []
    while it and pred(it):
        collect.append(next(it))
    return collect

class Indent:
    def __init__(self, depth=0):
        self._depth = int(depth)

    def depth(self):
        return self._depth

    def decrease_depth(self):
        self._depth -= 1
    
    def __str__(self):
        return '\\t{}'.format(self._depth)

class Newline:
    def __str__(self):
        return '\\n'

class Parens:
    def __init__(self, expr):
        self._expr = expr

    def expr(self):
        return self._expr

class Lexer:
    INDENT_RE = re.compile('^(\\t|\s{4})+')
    INDENT_WIDTH = 4

    def _keywords_to_ast(self, stc):
        it = iter(stc)
        node = SYN_TREE[next(it)]
        name = None

        for k in it:
            try:
                node = node[k]
            except KeyError:
                possible = ','.join(map(lambda x: '`{}`'.format(x), node.keys()))
                raise ParserError('expected one of {}. got `{}`'.format(possible, k))

        if '_op' not in node:
            raise ParserError('unexpected symbol `{}` in `{}`'.format(name, stc))

        return node['_op']

    def _interpret_buffer(self, buf: str):
        if buf == 'uzbl':
            return UzblConstant()
        elif buf == 'menge':
            return Menge()
        elif buf == 'liste':
            return Liste()
        elif buf in KEYWORDS:
            return Keyword(buf)
        elif buf.isnumeric():
            return Number(float(buf))
        else:
            parts = buf.split('.')
            if 1 < len(parts):
                return Access(parts)
            else:
                return Ident(buf)

    def _reduce_lex(self, it: peekable):
        reduced = []
        for lexem in it:
            if isof(lexem, Keyword):
                stc = take_while(it, lambda it: isof(it.peek(), Keyword))
                stc = [lexem.name(), *map(lambda kw: kw.name(), stc)]
                kw = self._keywords_to_ast(stc)
                reduced.append(kw())

            else:
                reduced.append(lexem)
        
        return reduced

    def _lex_source(self, it: peekable):
        lexed = []


        buf = ''
        for c in it:
            if c == ' ':
                pass

            elif c == '(':

                def parens_parser(init):
                    paren_stack = init
                    def predicate(it):
                        p = it.peek()
                        if p == '(':
                            paren_stack.append(p)
                        elif p == ')':
                            paren_stack.pop()
                            return 0 < len(paren_stack)
                        return True
                    return predicate

                sub = take_while(it, parens_parser(['(']))
                if it:
                    # drop trailing )
                    assert next(it) == ')'
                sub = self._lex_source(peekable(sub))
                lexed.append(Parens(sub))
                continue

            # parse strings here
            # TODO: discourage use of ' here
            elif c == '"' or c == "'":
                buf = take_while(it, lambda it: it.peek() != c)
                buf = ''.join(buf)
                lexed.append(String(buf))
                # drop trailing ' or "
                next(it)
                buf = ''
                continue

            else:
                buf += c
                continue

            if buf:
                out = self._interpret_buffer(buf)
                lexed.append(out)
                buf = ''

        if buf:
            out = self._interpret_buffer(buf)
            lexed.append(out)

        return self._reduce_lex(peekable(lexed))

    def lex(self, line: str):
        lexed = []

        match = self.INDENT_RE.match(line)
        if match:
            depth = match.span()[1]
            lexed.append(Indent(depth / self.INDENT_WIDTH))

        it = peekable(line.strip())
        lexed.extend(self._lex_source(it))

        return lexed

class Parser:
    def __init__(self):
        self._lexer = Lexer()
    
    def _parse_keyword(self, it):
        if isinstance(it, list):
            it = peekable(it)
        stc = take_while(it, peek_is(Keyword))
        if not stc:
            return None
        assert len(stc) == 1
        return stc.pop()

    def _take_block(self, lines, min_depth = 1):
        block = []
        while lines:
            next_line = lines.peek()

            # skip line if empty
            if not next_line:
                next(lines)
                continue

            if isof(next_line, Block):
                return next_line

            start = next_line[0]

            if not isof(start, Indent) or not min_depth <= start.depth():
                break

            next_line = next(lines)

            # drop indent
            next_line[0].decrease_depth()
            if next_line[0].depth() == 0:
                block.append(next_line[1:])
            else:
                block.append(list(next_line))
        return block

    def _parse_expression(self, line):
        stack = []
        if not isinstance(line, peekable):
            line = peekable(line)

        while line:
            token = next(line)

            if isof(token, Operator):
                if stack:
                    top = stack.pop()
                    if not (isof(top, Value) or isof(top, Operator)):
                        assert False
                    token.add_arg(top)
                
                stack.append(token)

            elif isof(token, Value):
                if stack:
                    if isof(stack[-1], Ident):
                        ident = stack.pop()
                        call = FunctionCall(ident)
                        call.add_arg(token)
                        stack.append(call)
                    else:
                        assert len(stack[-1].args()) < 2
                        stack[-1].add_arg(token)
                else:
                    stack.append(token)

            elif isof(token, Parens):
                sub = self._parse_expression(token.expr()) 
                if stack:
                    assert len(stack[-1].args()) < 2
                    stack[-1].add_arg(sub)
                else:
                    stack.append(sub)

            elif isof(token, Arguments):
                top = stack.pop()
                assert isof(top, Liste)
                pred = lambda it: peek_is(Value)(it) or peek_is(Ident)(it)
                args = take_while(line, pred)
                stack.append(Construct(top, args))

            elif isof(token, Readin):
                stack.append(token)

            else:
                raise ParserError('token `{}` not expected in this position'.format(token))

        if len(stack) != 1:
            print(stack)
            assert False

        return stack.pop()

    def _parse_declaration(self, line):
        name = next(line)
        args, markers = [], []

        while line:
            for kw in take_while(line, peek_is(Keyword)):
                if isof(kw, Arguments):
                    args = take_while(line, peek_is(Ident))
                elif isof(kw, Marker):
                    markers.append(kw)

        return (name, args, markers)

    def _parse_line(self, line, lines):
        line = peekable(line)
        item = next(line)

        if isof(item, Declaration):
            name, args, markers = self._parse_declaration(line)

            block = self._take_block(lines)
            block = self._parse_lines(block)

            item.set_name(name)
            item.set_args(args)
            item.set_block(block)

            for marker in markers:
                item.add_marker(marker)

        elif isof(item, Repeat):
            block = self._take_block(lines)
            block = self._parse_lines(block)
            item.set_block(block)

        elif isof(item, Branch):
            assert isof(item, If)

            condition = self._parse_expression(line)
            block = self._take_block(lines)
            block = self._parse_lines(block)

            item.add_branch(condition, block)

            if lines:
                cls = self._parse_keyword(lines.peek())
                try:
                    while isof(cls, Elif):
                        line = next(lines)
                        # drop elif keyword
                        line = line[1:]
                        condition = self._parse_expression(line)
                        block = self._take_block(lines)
                        block = self._parse_lines(block)
                        item.add_branch(condition, block)

                        cls = self._parse_keyword(lines.peek())
                    
                    if isof(cls, Else):
                        line = next(lines)
                        block = self._take_block(lines)
                        block = self._parse_lines(block)
                        item.set_default_branch(block)

                except StopIteration:
                    pass

        elif isof(item, Print) or isof(item, Readin):
            for arg in line:
                item.add_arg(self._parse_expression([arg]))

        elif isof(item, Use):
            for arg in line:
                assert isof(arg, Ident)
                item.add_arg(arg)

        elif isof(item, Value) or isof(item, Parens):
            if isof(item, Ident) and line and isof(line.peek(), Value):
                args = take_while(line, peek_is(Value))
                return FunctionCall(item, args)

            if isof(item, Parens):
                item = self._parse_expression(item.expr())

            kw = self._parse_keyword(line)
            if kw != None:
                if isof(kw, Return):
                    kw.add_arg(item)

                elif isof(kw, Statement):
                    val = self._parse_expression(line)

                    if isof(kw, LHAssign) and isof(item, Ident):
                        kw.set_ident(item)
                        kw.set_value(val)
                    elif isof(kw, RHAssign) and isof(val, Ident):
                        kw.set_ident(val)
                        kw.set_value(item)
                    else:
                        assert False

                return kw

            else:
                return item

        # drop empty indents
        elif isof(item, Indent):
            return None

        return item

    def _parse_lines(self, lines):
        block = Block()
        lines = peekable(lines)

        for line in lines:
            # skip empty lines
            if not line:
                continue

            if not isinstance(line, peekable):
                line = peekable(line)

            parsed = self._parse_line(line, lines)
            if not parsed is None:
                block.append(parsed)

        return block

    def parse(self, content: str) -> list:
        lexed = [peekable(self._lexer.lex(line)) for line in content.split('\n')]
        return self._parse_lines(lexed)
