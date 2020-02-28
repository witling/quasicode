from .program import Program

DEFUN = 10
FUN = DEFUN * 10

class OutOfOettingerException(Exception):
    pass

class Context:
    def __init__(self):
        self._globals = {}
        self._includes = []

        self._fun = 100
        self._loaded, self._locals, self._loops = [], [], []

    def __getitem__(self, key):
        self.defun()
        key = str(key)
        if self._locals and key in self._locals[-1][0]:
            return self._locals[-1][0][key]
        return self._globals[key]

    def __setitem__(self, key, value):
        self.defun()
        scope = self._locals[-1][0] if self._locals else self._globals
        scope[str(key)] = value

    def _search_file(self, name):
        import os

        name = str(name)

        for path in self._includes:
            if os.path.exists(path) and os.path.isdir(path):
                for fname in os.listdir(path):
                    front, fext = os.path.splitext(fname)
                    if not (fext == Program.FEXT or fext == Program.FEXTC):
                        continue
                    if front == name:
                        return os.path.join(path, fname)

        return None

    def add_include_path(self, path):
        self._includes.append(path)

    def load(self, program: Program):
        for use in program.uses():
            path = self._search_file(use)
            print(path)
            if not path:
                raise Exception('cannot use `{}`. not found'.format(str(use)))
            # TODO: allow loading non-compiled programs
            # TODO: avoid reimporting programs
            with open(path, 'rb') as f:
                self.load(Program.load(f))

        self._loaded.append(program)

    def loaded(self):
        return self._loaded

    def lookup(self, name):
        for loaded in self.loaded():
            if name in loaded:
                return loaded[name]
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

    def set_return(self, value):
        self._locals[-1][1](value)

    def push_locals(self, frame, rec_return):
        self._locals.append((frame, rec_return))

    def pop_locals(self):
        self._locals.pop()
