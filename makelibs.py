#!/usr/bin/python3

import os
from os.path import abspath, dirname, join, splitext
from shutil import copyfile, rmtree

from qclib import Interpreter, PythonLibrary

LIBRARY_BUILD = '/tmp/qclibs'
IGNORE = ['deps', '__pycache__']

def create_libraries():
    rmtree(LIBRARY_BUILD)
    os.makedirs(LIBRARY_BUILD)

    for script in os.listdir(join(dirname(__file__), 'lib')):
        fname, fext = splitext(script)

        if fname in IGNORE:
            continue

        import_path = 'lib.{}'.format(fname)
        sub = __import__(import_path)

    subclasses = PythonLibrary.__subclasses__()

    for cls in subclasses:
        name = cls.__module__.split('.')[-1]
        path = join(LIBRARY_BUILD, '{}.qcc'.format(name))
        instance = cls()
        with open(path, 'wb') as f:
            instance.save(f)

def install_libraries():
    for src in os.listdir(LIBRARY_BUILD):
        dst = join(Interpreter.LIB_PATH, src)
        src = join(LIBRARY_BUILD, src)
        copyfile(src, dst)

create_libraries()
install_libraries()
