from .generic import *

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

class LogicalAnd(Operator):
    def __init__(self):
        super().__init__()

class LogicalNot(Operator):
    def __init__(self):
        super().__init__()

    def run(self, ctx):
        return not self._args[0]

class LogicalOr(Operator):
    def __init__(self):
        super().__init__()

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
