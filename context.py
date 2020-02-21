class Context:
    def __init__(self):
        self._inner = {}

    def __getitem__(self, key):
        return self._inner[str(key)]

    def __setitem__(self, key, value):
        self._inner[str(key)] = value
