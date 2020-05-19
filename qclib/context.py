from .error import LookupException, OutOfOettingerException
from .frame import Frame
from .program import Library, Program

import sys

DEFUN = 10
FUN = DEFUN * 10

class Context:
    def __init__(self):
        self._stdin, self._stdout = sys.stdin, sys.stdout
        self._global = Frame(None)
        self._includes = []

        self._fun = 100
        self._loaded, self._stack = {}, [self._global]
        self._exit_code = 0

        self._funny_mode = True

        self.last_error = None

    def __getitem__(self, key):
        self.defun()
        frame = self.frame()
        key = str(key)

        if frame and key in frame:
            return frame[key]
        #if self._stack and key in self._stack[-1][0]:
        #    return self._stack[-1][0][key]

        try:
            return self.lookup(key)

        except LookupException:
            pass

        if not key in self._global:
            raise LookupException(key)

        return self._global[key]

    def __setitem__(self, key, value):
        self.defun()
        # if there is a last stack frame, assign to it
        frame = self.frame()
        key = str(key)
        if frame:
            frame[key] = value
        else:
            self._global[key] = value
        #scope = self._stack[-1][0] if self._stack else self._global
        #scope[str(key)] = value

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

    def frame(self):
        return self._stack[-1] if self._stack else None

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
        self.frame().push_loop(loop)
        #self._loops.append(loop)

    def pop_loop(self):
        self.frame().pop_loop()
        #self._loops.pop()

    def last_loop(self):
        #return self._loops[-1]
        return self.frame()._loops[-1]

    def set_return(self, value):
        if not self._stack:
            # TODO: implement handling of main function return
            pass
        self._stack[-1].set_return(value)

    def push_frame(self, frame):
        self._stack.append(frame)

    def pop_frame(self):
        self._stack.pop()

class RestrictedContext(Context):
    def __init__(self):
        super().__init__()
        self._allowed_modules = None
        self._blocked_modules = None

    def set_allowed_modules(self, ls):
        self._allowed_modules = ls

    def set_blocked_modules(self, ls):
        self._blocked_modules = ls

    def _load_postprocess(self, library):
        modname = library.modname()
        if not modname is None:
            if self._blocked_modules and modname in self._blocked_modules:
                raise Exception('usage of module `{}` is not permitted in this context.'.format(modname))

            if self._allowed_modules and not modname in self._allowed_modules:
                raise Exception('usage of module `{}` is not permitted in this context.'.format(modname))
