from .generic import *
from .liste import Liste
from .value import Ident, Menge

class Construct:
    def __init__(self, ty, init):
        self._ty = ty
        self._init = init

    def __str__(self):
        return '{}[{}]'.format(self._ty.__name__, ', '.join(repr(x) for x in self._init))

    def run(self, ctx):
        if self._ty is Liste:
            liste = self._ty()
            for item in self._init:
                if isof(item, Ident):
                    liste._val.append(item.run(ctx))
                else:
                    liste._val.append(item)
            return liste
        elif self._ty is Menge:
            # TODO: initialize object?
            return self._ty()
        raise Exception('unexpected type')

class Debug(Statement):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'debug'

    def run(self, ctx):
        from pudb import set_trace
        set_trace()

class Use(Statement, Parameterized):
    def __init__(self):
        Statement.__init__(self)
        Parameterized.__init__(self)

    def __str__(self):
        return 'use'

    def run(self, ctx):
        modname = self.args()[0]
        raise Exception('local use is not implemented :(')

class Exit(Statement):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'exit'

class Nop(NestedStatement):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'nop'

    def run(self, ctx):
        ctx.fun()

class Raise(NestedStatement):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'raise'

class Return(Statement, Parameterized):
    def __init__(self):
        Statement.__init__(self)
        Parameterized.__init__(self)

    def __str__(self):
        return 'return {}'.format(' '.join(map(str, self._args)))

    def run(self, ctx):
        ret = self.args()[0].run(ctx)
        ctx.set_return(ret)

class Repeat(NestedStatement):
    def __init__(self):
        super().__init__()
        self._broken = False
        self._predicate = lambda _: True

    def __str__(self):
        return super().__str__()

    def set_predicate(self, pred):
        self._predicate = pred

    def end(self):
        self._broken = True

    def run(self, ctx):
        ctx.push_loop(self)
        while not self._broken and self._predicate(ctx):
            for step in self.block():
                step.run(ctx)
                if self._broken:
                    break
        ctx.pop_loop()

class Break(NestedStatement):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'break'

    def run(self, ctx):
        ctx.last_loop().end()
