from .error import LookupException, OutOfOettingerException
from .program import Library, Program

import sys

DEFUN = 10
FUN = DEFUN * 10

class Context:
    def __init__(self):
        self._stdin, self._stdout = sys.stdin, sys.stdout
        self._globals = {}
        self._includes = []

        self._fun = 100
        self._loaded, self._locals, self._loops = {}, [], []
        self._exit_code = 0

        self._funny_mode = True

        self.last_error = None

    def __getitem__(self, key):
        self.defun()
        key = str(key)

        if self._locals and key in self._locals[-1][0]:
            return self._locals[-1][0][key]

        try:
            return self.lookup(key)

        except LookupException:
            pass

        if not key in self._globals:
            raise LookupException(key)

        return self._globals[key]

    def __setitem__(self, key, value):
        self.defun()
        # if there is a last stack frame, assign to it
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
    
    def _load_postprocess(self, library):
        pass

    def stdin(self):
        return self._stdin

    def set_stdin(self, stdin):
        self._stdin = stdin

    def stdout(self):
        return self._stdout

    def set_stdout(self, stdout):
        self._stdout = stdout

    def exit_code(self):
        return self._exit_code

    def set_exit_code(self, code):
        self._exit_code = code

    def is_funny_mode(self):
        return self._funny_mode

    def disable_funny_mode(self):
        self._funny_mode = False

    def add_include_path(self, path):
        self._includes.append(path)

    def load_by_name(self, name):
        path = self._search_file(name)
        if not path:
            raise LookupException(name)

        library = Library.load(path)

        self._load_postprocess(library)

        # TODO: avoid reimporting programs
        self.load(library)

    def load(self, program: Program):
        for use in program.uses():
            self.load_by_name(use)

        self._load_postprocess(program)

        self._loaded[program.modname()] = program

    def loaded(self):
        return self._loaded

    def locals(self):
        return self._locals[-1][0] if self._locals else None

    def lookup(self, name):
        for _, loaded in self.loaded().items():
            if name in loaded:
                return loaded[name]
        raise LookupException(name)

    def fun(self):
        if not self.is_funny_mode():
            return

        if self._fun <= 0:
            raise OutOfOettingerException
        if self._fun <= 75:
            self._fun += FUN

    def defun(self):
        if not self.is_funny_mode():
            return

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
        if not self._locals:
            # TODO: implement handling of main function return
            pass
        self._locals[-1][1](value)

    def push_locals(self, frame, rec_return):
        self._locals.append((frame, rec_return))

    def pop_locals(self):
        self._locals.pop()

class RestrictedContext(Context):
    def __init__(self):
        super().__init__()
        self._allowed_modules = None

    def set_allowed_modules(self, ls):
        self._allowed_modules = ls

    def _load_postprocess(self, library):
        modname = library.modname()
        if not modname is None:
            if self._allowed_modules and not modname in self._allowed_modules:
                raise Exception('usage of module `{}` is not permitted in this context.'.format(modname))
