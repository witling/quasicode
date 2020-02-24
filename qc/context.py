from program import Program

DEFUN = 10
FUN = DEFUN * 10

class OutOfOettingerException(Exception):
    pass

class Context:
    def __init__(self):
        self._inner = {}
        self._loaded = []
        self._locals = []
        self._loops = []

        self._fun = 100

    def __getitem__(self, key):
        self.defun()
        return self._inner[str(key)]

    def __setitem__(self, key, value):
        self.defun()
        self._inner[str(key)] = value

    def load(self, program: Program):
        self._loaded.append(program)

    def loaded(self):
        return self._loaded

    def lookup(self, name):
        for loaded in self.loaded():
            if name in loaded.idents():
                return loaded.idents()[name]
        return None

    def fun(self):
        if self._fun <= 0:
            raise OutOfOettingerException
        if self._fun <= 75:
            self._fun += FUN

    def defun(self):
        self._fun -= DEFUN
        if self._fun <= 0:
            raise OutOfOettingerException

    def push_loop(self, loop):
        self._loops.append(loop)

    def pop_loop(self):
        self._loops.pop()

    def last_loop(self):
        return self._loops[-1]

    def push_locals(self, frame):
        self._locals.append(frame)

    def pop_locals(self):
        self._locals.pop()
