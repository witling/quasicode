from .error import LookupException, OutOfOettingerException
from .program import Library, Program

import sys

DEFUN = 10
FUN = DEFUN * 10

class Context:
    def __init__(self):
        self._stdin, self._stdout = sys.stdin, sys.stdout
        self._includes = []

        self._fun = 100
        self._exit_code = 0

        self._funny_mode = True

        self.last_error = None

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

    def set_return(self, value):
        if not self._stack:
            # TODO: implement handling of main function return
            pass
        self._stack[-1].set_return(value)

    def is_load_allowed(self, name):
        return True

class RestrictedContext(Context):
    def __init__(self):
        super().__init__()
        self._allowed_modules = None
        self._blocked_modules = None

    def set_allowed_modules(self, ls):
        self._allowed_modules = ls

    def set_blocked_modules(self, ls):
        self._blocked_modules = ls

    def is_load_allowed(self, name):
        if self._blocked_modules and name in self._blocked_modules:
            return False

        if self._allowed_modules and not name in self._allowed_modules:
            return False

        return True
