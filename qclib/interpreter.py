from .ast import *
from .ast.generic import isof
from .const import *
from .context import *
from .program import *
from .std import *

import pylovm2

def try_py_module_load(name):
    import importlib
    import inspect
    try:
        pymod = importlib.import_module(name)
        members = inspect.getmembers(pymod, inspect.isfunction)
        module = pylovm2.ModuleBuilder.named(name)

        for key, value in members:
            module.add(key).pyfn(value)

        return module.build()
    except ImportError:
        return None

class Interpreter:
    def __init__(self, restricted=False):
        import os
        import os.path

        self._vm = pylovm2.Vm()

        self._ctx = Context() if not restricted else RestrictedContext()
        self._lovm2ctx = self._vm.ctx()
        self._lovm2ctx.clear_load_path()
        #self._lovm2ctx.add_load_path(os.getcwd())
        self._lovm2ctx.add_load_path(os.path.expanduser(USERLIB_PATH))
        self._lovm2ctx.add_load_path(LIB_PATH)

        def load_hook(name, relative_to):
            if not self._ctx.is_load_allowed(name):
                raise ImportError('usage of module `{}` is not permitted in this context.'.format(name))

            if name in STD_MODULE_MAP:
                return STD_MODULE_MAP[name](self._ctx)._module

            for fpath in self._lovm2ctx.load_path():
                if not os.path.exists(fpath):
                    continue

                for fname in os.listdir(fpath):
                    modname, ext = os.path.splitext(fname)
                    if modname != name:
                        continue

                    modpath = os.path.abspath(os.path.join(fpath, fname))
                    try:
                        return Library.load(modpath)._module
                    except Exception as e:
                        print(e)
            
            # TODO: can we implement this feature?
            #return try_py_module_load(name)

        self._vm.set_load_hook(load_hook)

        # load std library
        self._vm.load(StdLibrary(self._ctx)._module)

    def _run_func(self, func: Function, ctx: Context):
        last = None
        for step in func.block():
            last = step.run(ctx)
        return last

    def disable_funny_mode(self):
        self._ctx.disable_funny_mode()

    def load(self, program: Program):
        import os.path

        if not program._file is None:
            moddir = os.path.dirname(program._file)
            self._lovm2ctx.add_load_path(moddir)

        self._vm.load(program._module)
        #self._ctx.load(program)

    def call(self, name: str, *args):
        return self._vm.call(name, *args)
        #def to_quasi_value(val):
        #    if val.__class__ is Ident:
        #        return val
        #    return Value.create(val)
        #args = [to_quasi_value(arg) for arg in args]
        #call = FunctionCall(Ident(name), args)
        #return call.run(self._ctx)

    def run(self):
        try:
            self._vm.run()
            self._ctx.set_exit_code(0)
            return self._ctx.exit_code()
        except Exception as e:
            self._ctx.set_exit_code(1)
            raise e
        #try:
        #    for _, loaded in self._ctx.loaded().items():
        #        if not isof(loaded, Program):
        #            continue
        #        ep = loaded.entry_point()
        #        if ep:
        #            self._run_func(loaded[ep], self._ctx)
        #            break
        #    else:
        #        raise Exception('no starting point')

        #except Exception as e:
        #    import traceback
        #    self._ctx.set_exit_code(1)
        #    print(traceback.format_exc())
        #    print(e)

        #    self._ctx.last_error = e

        #return self._ctx.exit_code()
