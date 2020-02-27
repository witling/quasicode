from context import Context

def isof(var, cls) -> bool:
    return isinstance(var, cls) or any(isof(cls, b) for b in var.__class__.__bases__ if b.__name__ != 'object')

class Runnable:
    def run(self, ctx: Context):
        pass

class Parameterized:
    def __init__(self):
        self._args = []
    
    def args(self):
        return self._args

    def add_arg(self, arg):
        self._args.append(arg)

class Keyword:
    def __init__(self, name=None):
        self._name = name

    def name(self):
        return self._name

    def eq(self, other):
        if isinstance(other, str):
            return self._name == other
        if isof(other, Keyword):
            return self._name == other._name
        return False

    def __str__(self):
        return self.name()

class Statement(Keyword):
    def __init__(self):
        super().__init__()

class NestedStatement(Statement, Runnable):
    def __init__(self):
        self._block = Block()

    def block(self):
        return self._block

    def set_block(self, block):
        self._block = block

    def run(self, ctx: Context):
        for step in self._block:
            step.run(ctx)

    def __str__(self):
        return '\n'.join(map(str, self._block))

class Block(list, Runnable):
    def __init__(self):
        self._broken = False

    def __str__(self):
        return ' '.join(map(str, self))

    def end(self):
        self._broken = True

    def run(self, ctx: Context):
        last = None
        for step in self:
            if self._broken:
                break
            last = step.run(ctx)
        return last

class FunctionCall(Runnable, Parameterized):
    def __init__(self, name, args=[]):
        Parameterized.__init__(self)
        self._name = name
        for arg in args:
            self.add_arg(arg)

    def __str__(self):
        return '{} {}'.format(self.name(), ' '.join(map(str, self._args)))

    def name(self):
        return self._name.name()

    def run(self, ctx: Context):
        rvars = [arg.run(ctx) for arg in self.args()]
        decl = ctx.lookup(self.name())

        assert len(decl.args()) == len(rvars)
        frame = {k.name(): v for k, v in zip(decl.args(), rvars)}
        self._ret = None

        def receive_return(v):
            self._ret = v
            decl.block().end()

        ctx.push_locals(frame, receive_return)
        last = decl.block().run(ctx)
        ctx.pop_locals()

        if self._ret:
            return self._ret
        return last
