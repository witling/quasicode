#!/usr/bin/python3

import inspect
import os
import sys

from os.path import abspath, dirname, join, splitext
from shutil import copyfile, rmtree

from qclib import Interpreter, Program, Library

LIBRARY_BUILD = '/tmp/qclibs'
IGNORE = ['util', '__pycache__']

def prepare():
    try:
        rmtree(LIBRARY_BUILD)
    except FileNotFoundError:
        pass
    os.makedirs(LIBRARY_BUILD)

def create_libraries():
    prepare()

    folder = abspath(join(dirname(__file__), 'qclib/lib'))

    for script in os.listdir(folder):
        fname, fext = splitext(script)

        if fname in IGNORE:
            continue

        import_path = 'qclib.lib.{}'.format(fname)
        sub = __import__(import_path)

    subclasses = Library.__subclasses__()

    for cls in subclasses:
        fpath = inspect.getfile(cls)
        try:
            if fpath.index(folder) != 0:
                continue
        except ValueError:
            continue

        name = cls.__module__.split('.')[-1]
        path = join(LIBRARY_BUILD, '{}{}'.format(name, Program.FEXTC))
        instance = cls()
        with open(path, 'wb') as f:
            instance.save(f)

def install_libraries():
    if not os.path.exists(Interpreter.LIB_PATH):
        os.makedirs(Interpreter.LIB_PATH)

    for src in os.listdir(LIBRARY_BUILD):
        dst = join(Interpreter.LIB_PATH, src)
        src = join(LIBRARY_BUILD, src)
        copyfile(src, dst)

if __name__ == '__main__':
    create_libraries()
    install_libraries()
