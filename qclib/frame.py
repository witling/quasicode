class Frame(dict):
    def __init__(self, block, init_locals=None):
        super().__init__({} if init_locals is None else init_locals)
        self._block = block
        self._loops = []
        self._return = None
        self._has_returned = False

    def build(block, ctx, keys, values):
        var = {str(k): v.run(ctx) for k, v in zip(keys, values)}

        return Frame(block, var)

    def push_loop(self, ref):
        self._loops.append(ref)

    def pop_loop(self):
        self._loops.pop()

    def has_returned(self):
        return self._has_returned

    def set_return(self, value):
        self._return = value
        # stop execution of local loops
        for loop in self._loops:
            loop.end()
        # stop execution of coupled block
        self._has_returned = True
