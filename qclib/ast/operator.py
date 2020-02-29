from .generic import *
from .value import *

def foldtwo(fn, args, ctx):
    arg1 = args[0].run(ctx)
    arg2 = args[1].run(ctx)
    return fn(float(arg1), float(arg2))

class Operator(Keyword, Parameterized):
    def __init__(self):
        super().__init__()
        Parameterized.__init__(self)

    def __str__(self, name=''):
        return '({} {})'.format(name, ' '.join(map(str, self._args)))

class Compare(Operator):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        return self._args[0].run(ctx) == self._args[1].run(ctx)

    def __str__(self):
        return super().__str__('==')

class Less(Operator):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        return self._args[0].run(ctx) < self._args[1].run(ctx)

class LogicalAnd(Operator):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        return self._args[0].run(ctx) and self._args[1].run(ctx)

class LogicalNot(Operator):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        return not self._args[0].run(ctx)

class LogicalOr(Operator):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        if self._args[0].run(ctx):
            return Value.create(True)
        if self._args[1].run(ctx):
            return Value.create(True)
        return Value.create(False)

class Add(Operator):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        return foldtwo(lambda a, b: a + b, self._args, ctx)

    def __str__(self):
        return super().__str__('+')

class Sub(Operator):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        return foldtwo(lambda a, b: a - b, self._args, ctx)

    def __str__(self):
        return super().__str__('-')

class Mul(Operator):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        return foldtwo(lambda a, b: a * b, self._args, ctx)

    def __str__(self):
        return super().__str__('*')

class Div(Operator):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        return foldtwo(lambda a, b: a / b, self._args, ctx)

    def __str__(self):
        return super().__str__('/')

class Mod(Operator):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        return foldtwo(lambda a, b: a % b, self._args, ctx)

    def __str__(self):
        return super().__str__('modulo')
