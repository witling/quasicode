from ..error import RuntimeException
from ..frame import Frame

def isof(var, cls) -> bool:
    return isinstance(var, cls) or any(isof(cls, b) for b in var.__class__.__bases__ if b.__name__ != 'object')

def decl_key(k):
    if isinstance(k, str):
        return k
    if hasattr(k, 'name'):
        return k.name()
    raise Exception('variable `{}` is not valid as function argument'.format(k))

class Runnable:
    def run(self, ctx):
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
        if self._name is None:
            self._name = self.__class__.__name__

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

class Arguments(Keyword):
    def __init__(self):
        super().__init__()

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

    def run(self, ctx):
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

    def run(self, ctx):
        self._broken = False
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

    def _call_builtin(self, decl, ctx):
        keys = (i for i in range(len(self.args())))
        frame = Frame.build(decl.block(), ctx, keys, self.args())

        ctx.push_frame(frame)
        ret = decl.run(ctx)
        ctx.pop_frame()

        if None != frame._return:
            return frame._return
        return ret

    def _call(self, decl, ctx):
        exparg, gotarg = len(decl.args()), len(self.args())

        if exparg != gotarg:
            raise Exception('call to `{}` expected {} arguments, got {}'.format(self.name(), exparg, gotarg))

        keys = map(decl_key, decl.args())
        frame = Frame.build(decl.block(), ctx, keys, self.args())

        ctx.push_frame(frame)
        last = decl.block().run(ctx)
        ctx.pop_frame()

        if None != frame._return:
            return frame._return
        return last

    def run(self, ctx):
        decl = ctx[self.name()]

        if hasattr(decl, 'is_builtin'):
            #raise RuntimeException('`{}` is not callable'.format(decl))

            if decl.is_builtin():
                return self._call_builtin(decl, ctx)
            return self._call(decl, ctx)

        else:
            # FIXME: is this the correct behavior?
            return decl
