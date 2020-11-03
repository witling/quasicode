#!/usr/bin/python3

import os

from os.path import abspath, basename, dirname, expanduser, join, splitext
from shutil import copyfile, rmtree

from qclib import Interpreter, Library
from qclib.const import LIB_PATH, USERLIB_PATH

def build_libraries(folder, ignore=[]):
    libs = []

    # ignore hidden files
    for script in (path for path in os.listdir(folder) if not path.startswith('.')):
        if script in ignore:
            continue

        fpath = join(folder, script)
        lib = Library.load(fpath)
        libs.append(lib)

    return libs

def install_library(lib, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    fname = '{}{}'.format(lib._module.name(), Library.FEXTC)
    dst = join(dst_dir, fname)
    lib.save(dst)

DEFAULT_IGNORE = ['__pycache__', '__init__.py']

def process(
    src_dir,
    dst_dir=None,
    ignore=[]
):
    ignore.extend(DEFAULT_IGNORE)

    if dst_dir is None:
        dst_dir = expanduser(USERLIB_PATH)

    dst_dir = abspath(dst_dir)
    src_dir = abspath(src_dir)

    for lib in build_libraries(src_dir, ignore):
        print('installing', lib._module.name(), '...')
        install_library(lib, dst_dir)

    print('done.')

if __name__ == '__main__':
    main()
