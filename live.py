#!/usr/bin/python3

def main():
    import sys

    if len(sys.argv) <= 1:
        print('no file given')
        exit()

    from os.path import abspath, dirname, join

    confname = '{}/.env'.format(dirname(abspath(__file__)))
    with open(confname, 'r') as conf:
        for line in conf.read().split('\n'):
            try:
                key, val = line.split('=')
                if key == 'PYLOVM2_DEV_LOCATION':
                    sys.path.insert(0, val)
            except ValueError:
                pass

    sys.path.insert(0, abspath(join(dirname(__file__), '..')))
    from qclib import Compiler, Interpreter

    program = Compiler().compile_file(sys.argv[1])

    interpreter = Interpreter()
    interpreter.disable_funny_mode()
    interpreter.load(program)
    interpreter.run()

if __name__ == '__main__':
    main()
