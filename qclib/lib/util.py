try:
    from qclib import *
except:
    from os.path import abspath, dirname, join
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    from qclib import *

def create(name, fn):
    return PythonFunction(name, fn)

def create_const(name, fn):
    return PythonFunction(name, fn)
