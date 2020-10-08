"""
Module to define the array model for APL.
"""

class APLArray:
    def __init__(self, shape, data):
        self.shape = shape
        self.data = data

    @staticmethod
    def _str_format_n(n):
        if n < 0:
            return f"¯{APLArray._str_format_n(-n)}"
        if int(n) == n:
            return str(int(n))
        else:
            return str(n)
        
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
