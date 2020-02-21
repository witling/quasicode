from program import Program

class Interpreter:
    def __init__(self):
        self._loaded = []

    def load(self, program: Program):
        self._loaded.append(program)

    def run(self):
        for loaded in self._loaded:
            if loaded.entry_point():
                print('starting...')
                break
        else:
            print('no starting point.')
