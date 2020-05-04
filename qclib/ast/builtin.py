from .generic import *

class Print(Statement, Parameterized):
    def __init__(self):
        Statement.__init__(self)
        Parameterized.__init__(self)

    def run(self, ctx):
        print(' '.join(map(lambda x: str(x.run(ctx)), self._args)))

    def __str__(self):
        return 'print {}'.format(' '.join(map(str, self._args)))

class Construct(Statement, Parameterized):
    def __init__(self):
        Statement.__init__(self)
        Parameterized.__init__(self)

    def run(self, ctx):
        print('constructing', self._args)

    def __str__(self):
        return 'construct object'

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
