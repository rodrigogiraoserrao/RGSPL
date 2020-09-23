"""
Module to define the array model for APL.
"""

class APLArray:
    def __init__(self, shape, data):
        self.shape = shape
        self.data = data

    def __str__(self):
        return f"{self.shape} :: {self.data}"

    __repr__ = __str__

    def __eq__(self, other):
        return (
            isinstance(other, APLArray) and
            self.shape == other.shape and
            self.data == other.data
        )
