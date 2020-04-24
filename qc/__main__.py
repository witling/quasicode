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

def main():
    parser = argparse.ArgumentParser(
        description='Runtime for quasicode. The best language around.'
    )

    parser.add_argument('program', metavar='PROGRAM', type=str, help='the quasicode program to run.')
    parser.add_argument('--listing', action='store_true', default=False, help='printout the program before running.')
    parser.add_argument('--debug', action='store_true', default=False, help='enable interpreter debugging.')
    parser.add_argument('--nichluschdich', action='store_true', default=False, help='disable the funny mode.')

    args = parser.parse_args()

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

if __name__ == '__main__':
    main()
