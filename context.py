class Context:
    def __init__(self):
        self._inner = {}
        self._loops = []

    def __getitem__(self, key):
        return self._inner[str(key)]

    def __setitem__(self, key, value):
        self._inner[str(key)] = value

    def push_loop(self, loop):
        self._loops.append(loop)

    def pop_loop(self):
        self._loops.pop()

    def last_loop(self):
        return self._loops[-1]
