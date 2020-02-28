from .generic import *

class Branch(NestedStatement, Runnable):
    def __init__(self):
        self._branches = []
        self._default_branch = None

    def branches(self):
        return [*self._branches, (None, self._default_branch)] if self._default_branch else self._branches

    def add_branch(self, condition, block):
        self._branches.append((condition, block))

    def set_default_branch(self, block):
        self._default_branch = block

    def run(self, ctx):
        for condition, block in self._branches:
            if condition.run(ctx):
                block.run(ctx)
                break
        else:
            if self._default_branch:
                self._default_branch.run(ctx)

    def __str__(self):
        fixed = list(map(lambda x: '| {} -> {}'.format(x[0], x[1]), self._branches))
        if self._default_branch:
            fixed.append('| -> {}'.format(self._default_branch))
        return '\n'.join(fixed)

class If(Branch):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'if:\n' + super().__str__()

class Elif(Branch):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'elif'

class Else(Branch):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'else'
