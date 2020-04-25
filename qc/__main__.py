import argparse
import sys

try:
    from qclib import *
except:
    from os.path import abspath, dirname, join
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    from qclib import *

def load_source(fname):
    with open(fname, 'r') as src:
        return src.read()

def retrieve_program(fname):
    from os.path import splitext

    _, fext = splitext(fname)

    if fext == Program.FEXT:
        src = load_source(fname)
        compiler = Compiler()
        return compiler.compile(src)

    elif fext == Program.FEXTC:
        return Program.load(fname)

    raise Exception('unsupported file extension')

def argument_parser():
    parser = argparse.ArgumentParser(
        description='Runtime for quasicode. The best language around.'
    )
    subparser = parser.add_subparsers()

    parser_run = subparser.add_parser('run', help='run a quasicode program')
    parser_run.add_argument('program', metavar='PROGRAM', type=str, help='the quasicode program to run.')
    parser_run.add_argument('--listing', action='store_true', default=False, help='printout the program before running.')
    parser_run.add_argument('--debug', action='store_true', default=False, help='enable interpreter debugging.')
    parser_run.add_argument('--nichluschdich', action='store_true', default=False, help='disable the funny mode.')

    parser_install = subparser.add_parser('install', help='install a library.')
    parser_install.add_argument('library', metavar='LIBRARY', type=str, help='path to the library to install.')
    parser_install.add_argument('--ignore', type=str, default=[], nargs='+', help='files to ignore')

    return parser

def run(args):
    program = retrieve_program(args.program)
    interpreter = Interpreter()
    
    if args.listing:
        print('=== Listing', '=' * 8)
        print(program)
        print('=' * 20)

    if args.debug:
        from pudb import set_trace
        set_trace()

    if args.nichluschdich:
        interpreter.disable_funny_mode()

    interpreter.load(program)
    interpreter.run()

def install(args):
    from .makelibs import process
    from os.path import abspath

    process(
        src_dir=args.library,
        ignore=args.ignore
    )

def main():
    args = argument_parser().parse_args()

    if 'program' in args:
        run(args)

    elif 'library' in args:
        install(args)

    else:
        print('no command specified.')

if __name__ == '__main__':
    main()
