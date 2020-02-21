from .marker import *

class Branch(NestedStatement, Runnable):
    def __init__(self):
        self._branches = []
        self._default_branch = None

    def add_branch(self, condition, block):
        self._branches.append((condition, block))

    def set_default_branch(self, block):
        self._default_branch = block

    def run(self, ctx: Context):
        for condition, block in self._branches:
            if condition.run(ctx):
                block.run(ctx)
                break
        else:
            if self._default_branch:
                self._default_branch.run(ctx)

    def __str__(self):
        fixed = map(lambda x: '{} -> {}', self._branches)
        if self._default_branch:
            fixed.append('-> {}'.format(self._default_branch))
        return '\n'.join(fixed)

class If(Branch):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'if'

class Elif(Branch):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'elif'
