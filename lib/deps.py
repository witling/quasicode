try:
    from qclib import *
except:
    from os.path import abspath, dirname, join
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    from qclib import *
