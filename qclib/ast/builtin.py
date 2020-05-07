from .generic import *
from .value import Ident, Liste

class Construct(Parameterized):
    def __init__(self, ty, init):
        self._ty = ty
        self._init = init

    def run(self, ctx):
        if isof(self._ty, Liste):
            liste = self._ty
            for item in self._init:
                if isof(item, Ident):
                    liste._val.append(item.run(ctx))
                else:
                    liste._val.append(item)
            return liste
        raise Exception('unexpected type')

class Readin(Statement, Parameterized):
    RESPONSES = ['verstehe.', 'gut.', 'okay.', 'perfekt.']

    def __init__(self):
        Statement.__init__(self)
        Parameterized.__init__(self)

    def run(self, ctx):
        question = ' '.join(map(str, self.args()))

        ctx.stdout().write(question)
        ctx.stdout().flush()

        ret = ctx.stdin().readline()

        if ctx.is_funny_mode():
            from random import choice
            ctx.stdout().write('{}\n'.format(choice(Readin.RESPONSES)))
            ctx.stdout().flush()

        return ret

    def __str__(self):
        return 'stdin_read {}'.format(' '.join(map(str, self.args())))

class Print(Statement, Parameterized):
    def __init__(self):
        Statement.__init__(self)
        Parameterized.__init__(self)

    def run(self, ctx):
        msg = ' '.join(map(lambda x: str(x.run(ctx)), self._args)) + '\n'
        ctx.stdout().write(msg)
        ctx.stdout().flush()

    def __str__(self):
        return 'print {}'.format(' '.join(map(str, self._args)))

class Debug(Statement):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        from pudb import set_trace
        set_trace()

    def __str__(self):
        return 'debug'

class Use(Statement, Parameterized):
    def __init__(self):
        Statement.__init__(self)
        Parameterized.__init__(self)

    def run(self, ctx):
        modname = self.args()[0]
        raise Exception('local use is not implemented :(')

    def __str__(self):
        return 'use'

class Exit(Statement):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'exit'

class Nop(NestedStatement):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        ctx.fun()

    def __str__(self):
        return 'nop'

class Raise(NestedStatement):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'raise'

class Return(Statement, Parameterized):
    def __init__(self):
        Statement.__init__(self)
        Parameterized.__init__(self)

    def run(self, ctx):
        ctx.set_return(self.args()[0].run(ctx))

    def __str__(self):
        return 'return {}'.format(' '.join(map(str, self._args)))

class Repeat(NestedStatement):
    def __init__(self):
        super().__init__()
        self._broken = False

    def end(self):
        self._broken = True

    def run(self, ctx):
        ctx.push_loop(self)
        while not self._broken:
            for step in self.block():
                step.run(ctx)
                if self._broken:
                    break
        ctx.pop_loop()

    def __str__(self):
        return super().__str__()

class Break(NestedStatement):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        ctx.last_loop().end()

    def __str__(self):
        return 'break'
