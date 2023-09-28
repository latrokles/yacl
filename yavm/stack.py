
class Stack:
    def __init__(self, data=None):
        if data is None:
            data = []
        self._data = data

    @property
    def length(self):
        return len(self._data)

    def push(self, value):
        self._data.append(value)

    def pop(self):
        return self._data.pop()

    def peek(self):
        return self._data[-1]

    def is_empty(self):
        return self.length == 0

    def is_not_empty(self):
        return self.length > 0


