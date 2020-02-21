from .marker import *

class Print(Statement, Parameterized):
    def __init__(self):
        super().__init__()

    def run(self, ctx: Context):
        print(' '.join(map(lambda x: str(x.run(ctx)), self._args)))

    def __str__(self):
        return 'print {}'.format(' '.join(map(str, self._args)))

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

class Raise(NestedStatement):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'raise'

class Return(Statement, Parameterized):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'return {}'.format(' '.join(map(str, self._args)))

class Repeat(NestedStatement):
    def __init__(self):
        super().__init__()
        self._broken = False

    def run(self, ctx: Context):
        while not self._broken:
            super().run(ctx)

    def __str__(self):
        return 'repeat'

class Break(NestedStatement):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'break'
