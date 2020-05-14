from .generic import Runnable
from .value import Value

def normalize_index(key):
    if key is None:
        return key
    return int(key) - 1

class Liste(Value):
    def __init__(self, init=[]):
        super().__init__(init)

    def __getitem__(self, key):
        return self._val[normalize_index(key)]

    def __setitem__(self, key, value):
        self._val[normalize_index(key)] = value

    def run(self, ctx):
        return self

    def __str__(self):
        return str(self._val)

class Index(Runnable):
    def __init__(self, target, index):
        self._index = index
        self._target = target

    def eval(self, ctx):
        target = self.target().run(ctx)
        index = self.index().run(ctx)
        return target, index

    def run(self, ctx):
        target, index = self.eval(ctx)
        return target[index]

    def target(self):
        return self._target

    def index(self):
        return self._index

class Slice(Runnable):
    def __init__(self, start=None, end=None):
        self._start = start
        self._end = end

    def eval(self, ctx):
        target = self.target().run(ctx)
        start, end = self.range()
        start, end = start.run(ctx), end.run(ctx)
        return target, (start, end)

    def run(self, ctx):
        target, (start, end) = self.eval(ctx)
        assert not (start is None or end is None)

        start = normalize_index(start)
        end = normalize_index(end)

        if not start is None:
            start = int(start) - 1
            ls = target[start:]
        elif not end is None:
            ls = target[:end]
        else:
            ls = target[start:end]

        return Liste(ls)

    def target(self):
        return self._target

    def range(self):
        return (self._start, self._end)
