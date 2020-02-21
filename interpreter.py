from program import Program

class Interpreter:
    def __init__(self):
        self._loaded = []

    def load(self, program: Program):
        self._loaded.append(program)

    def _run_func(self, func):
        for step in func.block():
            step.run()

    def run(self):
        for loaded in self._loaded:
            ep = loaded.entry_point()
            if ep:
                self._run_func(loaded.idents()[ep])
                break
        else:
            print('no starting point.')
            return
