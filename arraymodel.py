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

    def is_simple(self):
        return (not self.shape) and (not isinstance(self.data, APLArray))

    @staticmethod
    def _simple_scalar_str(s):
        if isinstance(s, complex):
            return "J".join(map(APLArray._simple_scalar_str, [s.real, s.imag]))
        elif int(s) == s:
            return str(int(s))
        else:
            return str(s)

    def __str__(self):
        # Print simple scalars nicely.
        if self.is_simple():
            return APLArray._simple_scalar_str(self.data)

        # Print simple arrays next.
        if all(d.is_simple() for d in self.data):
            strs = list(map(str, self.data))
            maxw = max(map(len, strs))
            # Pad everything in array of rank 2 or more.
            rank = len(self.shape)
            if rank > 1:
                strs = map(lambda s: (maxw-len(s))*" " + s, strs)
            # We add as many newlines as dimensions we just completed.
            cumulative_dim_sizes = [math.prod(self.shape[-i-1:]) for i in range(rank-1)]
            string = ""
            for i, s in enumerate(strs):
                string += sum(i!=0 and 0 == i%l for l in cumulative_dim_sizes)*"\n"
                string += s + " "
            return string

        # Print nested vectors next
        if len(self.shape) == 1:
            strs = map(str, self.data)
            if all(d.is_simple() for d in self.data):
                return " ".join(strs)
            else:
                mid = " │ ".join(strs)
                top = "┌─"
                for char in mid:
                    top += "┬" if char == "│" else "─"
                top += "─┐"
                return top + "\n│ " + mid + " │\n└─" + top[2:-2].replace("┬", "┴") + "─┘"

        return f"{self.shape} :: {' '.join(map(str, self.data))}"

    __repr__ = __str__

    def __eq__(self, other):
        return (
            isinstance(other, APLArray) and
            self.shape == other.shape and
            self.data == other.data
        )
