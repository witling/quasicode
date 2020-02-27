import os

from qc import Compiler

LIB_PATH = '/usr/local/lib/quasicode'

if not os.path.exists(LIB_PATH):
    os.mkdir(LIB_PATH)

def install_lib(path):
    path = os.path.abspath(path)
    compiler = Compiler()

    for libfile in os.listdir(path):
        libfile = os.path.join(path, libfile)
        print(libfile)

install_lib(os.path.join(os.path.dirname(__file__), 'qc/lib'))
