from .generic import Runnable
from .value import Value

def normalize_index(key):
    if key is None:
        return key
    return int(key) - 1

class Liste(Value):
    def __init__(self, init=None):
        super().__init__(init if not init is None else [])

    def __getitem__(self, key):
        # slicing should be done through `Slice`
        assert not key.__class__ is slice
        return self._val[normalize_index(key)]

    def __setitem__(self, key, value):
        self._val[normalize_index(key)] = value

    def __len__(self):
        return len(self._val)

    def __str__(self):
        return str(self._val)

    def run(self, ctx):
        return self

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
    def __init__(self, target, start=None, end=None):
        self._target = target
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

        target = target._val
        start = normalize_index(start)
        end = normalize_index(end)

        if not (start is None or end is None):
            ls = target[start:end]
        elif not start is None:
            ls = target[start:]
        elif not end is None:
            ls = target[:end]

        return Liste(ls)

    def target(self):
        return self._target

    def range(self):
        return (self._start, self._end)
