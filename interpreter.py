from program import Program

class Interpreter:
    def __init__(self):
        self._loaded = []

    def load(self, program: Program):
        self._loaded.append(program)

    def run(self):
        pass
