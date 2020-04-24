#!/usr/bin/python3

import inspect
import os
import random
import sys

from os.path import abspath, dirname, expanduser, join, splitext
from shutil import copyfile, rmtree

from qclib import Interpreter, Program, Library

def random_id(n=6):
    sample = random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', n)
    return ''.join(sample)

LIBRARY_BUILD = '/tmp/qclibs_{}'.format(random_id())
IGNORE = ['util', '__pycache__']

def prepare():
    assert not os.path.exists(LIBRARY_BUILD)
    os.makedirs(LIBRARY_BUILD)

def cleanup():
    try:
        rmtree(LIBRARY_BUILD)
    except FileNotFoundError:
        pass
    except PermissionError:
        print('insufficient permissions to remove file')
        exit()

def create_libraries():
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

def install_libraries(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for src in os.listdir(LIBRARY_BUILD):
        dst = join(directory, src)
        src = join(LIBRARY_BUILD, src)
        copyfile(src, dst)

def main():
    prepare()
    create_libraries()

    directory = expanduser(Interpreter.USERLIB_PATH)
    install_libraries(directory)

    cleanup()

if __name__ == '__main__':
    main()
