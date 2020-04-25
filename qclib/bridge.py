import importlib

class Bridge:
    """
    this is a wrapper for builtin python functions. a reference will be passed to `PyLibrary` in order
    to work correctly
    """
    def vbreakpoint(self):
        import pudb
        pudb.set_trace()

    def vdebug(self, obj):
        import inspect
        print(inspect.getmembers(obj))

    def vprint(self, *args):
        print(*arg)

    def vimport(self, modname, ref):
        mod = importlib.import_module(modname)
        return
        if not scope is None:
            scope[modname] = mod
