#!/usr/bin/python3

import inspect
import os
import random
import sys

from os.path import abspath, dirname, expanduser, join, splitext
from shutil import copyfile, rmtree

from qclib import Interpreter, Program, Library
from qclib.library import Library, init_vlib, get_vlib_modname

def random_id(n=6):
    sample = random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', n)
    return ''.join(sample)

LIBRARY_BUILD = '/tmp/qclibs_{}'.format(random_id())
DEFAULT_IGNORE = ['__pycache__', '__init__.py']

def prepare(build_dir):
    assert not os.path.exists(build_dir)
    os.makedirs(build_dir)

def cleanup(build_dir):
    try:
        rmtree(build_dir)

    except FileNotFoundError:
        print('cannot cleanup dir. not found.')

    except PermissionError:
        print('insufficient permissions to remove file')
        exit()

def build_libraries(folder, ignore=[]):
    import importlib.util

    init_vlib()

    for script in os.listdir(folder):
        fname, _ = splitext(script)

        if script in ignore:
            continue

        fpath = join(folder, script)
        modname = get_vlib_modname(fname)

        spec = importlib.util.spec_from_file_location(modname, fpath)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        init_vlib(modname, mod)

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
        instance.save(path)

def install_libraries(build_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for src in os.listdir(build_dir):
        dst = join(dst_dir, src)
        src = join(build_dir, src)
        copyfile(src, dst)

def process(
    src_dir,
    dst_dir=None,
    ignore=[]
):
    ignore.extend(DEFAULT_IGNORE)
    build_dir = LIBRARY_BUILD
    src_dir = abspath(src_dir)

    if dst_dir is None:
        dst_dir = expanduser(Interpreter.USERLIB_PATH)

    prepare(build_dir)

    build_libraries(src_dir, ignore)
    install_libraries(build_dir, dst_dir)

    cleanup(build_dir)

if __name__ == '__main__':
    main()
