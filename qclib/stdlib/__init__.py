from ..error import AssertException
from ..library import *

from .bot import *

from urllib import request
import math
import random

class StdLibrary(Library):
    RESPONSES = ['verstehe.', 'gut.', 'okay.', 'perfekt.']

    def __init__(self, ctx):
        self._ctx = ctx

        module = pylovm2.ModuleBuilder.named('std')
        module.add('assert').pyfn(self._assert)
        module.add('bitte?').pyfn(self._bitte)
        module.add('quasi').pyfn(self._quasi)

        super().__init__(module.build())

    def _assert(self, *args):
        assert args[0]

    def _bitte(self, *args):
        question = ' '.join(map(str, args))

        self._ctx.stdout().write(question)
        self._ctx.stdout().flush()

        ret = self._ctx.stdin().readline()
        # drop newline char
        ret = ret[:-1]

        if self._ctx.is_funny_mode():
            from random import choice
            self._ctx.stdout().write('{}\n'.format(choice(StdLibrary.RESPONSES)))
            self._ctx.stdout().flush()

        return ret

    def _quasi(self, *args):
        msg = ' '.join(map(str, args)) + '\n'
        self._ctx.stdout().write(msg)
        self._ctx.stdout().flush()

class IoLibrary(Library):
    def __init__(self, ctx):
        self._ctx = ctx
        module = pylovm2.ModuleBuilder.named('io')
        module.add('inhaliere').pyfn(self._read)
        module.add('schreibe').pyfn(self._write)
        super().__init__(module.build())

    def _read(self, path):
        with open(path.to_py(), 'r') as fp:
            return fp.read()

    def _write(self, path, content):
        with open(path.to_py(), 'w') as fp:
            fp.write(content.to_py())

class ListLibrary(Library):
    def __init__(self, ctx):
        self._ctx = ctx
        module = pylovm2.ModuleBuilder.named('liste')
        module.add('länge').pyfn(self._len)
        module.add('lösche').pyfn(self._delete)
        module.add('push').pyfn(self._push)
        module.add('pop').pyfn(self._pop)
        module.add('pop_front').pyfn(self._pop_front)
        super().__init__(module.build())

    def _len(self, ls):
        return len(ls)

    def _delete(self, ls, idx):
        del ls[idx]

    def _push(self, ls, item):
        idx = len(ls)
        ls[idx] = item

    def _pop(self, ls):
        idx = len(ls) - 1
        item = ls[idx]
        del ls[idx]
        return item

    def _pop_front(self, ls):
        if 0 < len(ls):
            first = ls[0]
            del ls[0]
            return first

class MathLibrary(Library):
    def __init__(self, ctx):
        self._ctx = ctx
        module = pylovm2.ModuleBuilder.named('math')
        module.add('ceil').pyfn(self._ceil)
        module.add('floor').pyfn(self._floor)
        module.add('random').pyfn(self._rnd)
        module.add('sqrt').pyfn(self._sqrt)
        super().__init__(module.build())

    def _ceil(self, arg1: float):
        return math.ceil(arg1)

    def _floor(self, arg1: float):
        return math.floor(arg1)

    def _sqrt(self, arg1: float):
        return math.sqrt(arg1)
    
    def _rnd(self):
        return random.random()

class NetLibrary(Library):
    def __init__(self, ctx):
        self._ctx = ctx
        module = pylovm2.ModuleBuilder.named('net')
        module.add('ziehe').pyfn(self._download)
        super().__init__(module.build())

    def _download(self, url):
        req = request.urlopen(str(url))
        if req.msg == 'OK':
            return req.read().decode('utf8')
        return False

class StringLibrary(Library):
    def __init__(self, ctx):
        self._ctx = ctx
        module = pylovm2.ModuleBuilder.named('string')
        module.add('concat').pyfn(self._concat)
        module.add('format').pyfn(self._format)
        super().__init__(module.build())

    def _concat(self, first, second):
        return str(first) + str(second)

    def _format(self, template, arg):
        return str(template).format(str(arg))

STD_MODULE_MAP = {
    'bot': BotLibrary,
    'io': IoLibrary,
    'liste': ListLibrary,
    'math': MathLibrary,
    'net': NetLibrary,
    'string': StringLibrary,
}
