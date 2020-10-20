"""
Module to define the array model for APL.
"""

import math

class APLArray:
    def __init__(self, shape, data):
        self.shape = shape
        self.data = data

    def major_cells(self):
        if len(self.shape) == 0:
            return [self.data]
        elif len(self.shape) == 1:
            return self.data
        else:
            size = math.prod(self.shape)/self.shape[0]
            return [
                APLArray(self.shape[1:], self.data[i*size:(i+1)*size])
                for i in range(self.shape[0])
            ]
        
    def __str__(self):
        if isinstance(self.data, (float, int)):
            return self._str_format_n(self.data)
        elif isinstance(self.data, complex):
            return f"{self._str_format_n(self.data.real)}J{self._str_format_n(self.data.imag)}"
        else:
            return f"{self.shape} :: {' '.join(map(str, self.data))}"

    __repr__ = __str__

    def __eq__(self, other):
        return (
            isinstance(other, APLArray) and
            self.shape == other.shape and
            self.data == other.data
        )
