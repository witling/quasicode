from context import Context

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

class Statement:
    pass

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

class Block(list, Runnable):
    def __str__(self):
        return ' '.join(map(str, self))

    def run(self, ctx: Context):
        last = None
        for step in self:
            last = step.run(ctx)
        return last

class Marker:
    pass

class ConstMarker(Marker):
    pass

class MainMarker(Marker):
    pass

class SoMarker(Marker):
    pass
