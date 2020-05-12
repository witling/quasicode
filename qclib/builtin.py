from .ast import Block
from .function import Function

class ReadFn(Function):
    RESPONSES = ['verstehe.', 'gut.', 'okay.', 'perfekt.']

    def __init__(self):
        super().__init__([], Block())

    def __str__(self):
        return 'bitte?'

    def block(self):
        return self

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

class WriteFn(Function):
    def __init__(self):
        super().__init__([], Block())

    def __str__(self):
        return 'quasi'

    def block(self):
        return self

    def run(self, ctx):
        msg = ' '.join(map(lambda x: str(x.run(ctx)), self._args)) + '\n'
        ctx.stdout().write(msg)
        ctx.stdout().flush()
