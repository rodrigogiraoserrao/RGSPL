"""
Module to define the array model for APL.
"""

import math

class APLArray:
    def __init__(self, shape, data):
        self.shape = shape
        self.data = data

    def major_cells(self):
        """Returns an array with the major cells of self (as APLArray instances)."""
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

    def __str__(self):
        # Print simple scalars nicely.
        if self.is_simple():
            return _simple_scalar_str(self.data)

        # Print simple arrays next.
        if self.shape and all(d.is_simple() for d in self.data):
            strs = list(map(str, self.data))
            rank = len(self.shape)
            if rank > 1:
                widths = [0 for _ in range(self.shape[-1])]
                for i, s in enumerate(strs):
                    idx = i%self.shape[-1]
                    widths[idx] = max(widths[idx], len(s))
                for i, s in enumerate(strs):
                    # Pad left with required number of spaces.
                    strs[i] = (widths[i%self.shape[-1]]-len(s))*" " + s
            # Pad everything in array of rank 2 or more.
            # We add as many newlines as dimensions we just completed.
            cumulative_dim_sizes = [math.prod(self.shape[-i-1:]) for i in range(rank-1)]
            string = " "
            for i, s in enumerate(strs):
                string += sum(i!=0 and 0 == i%l for l in cumulative_dim_sizes)*"\n "
                string += s + " "
            return string

        # Print nested arrays next.
        # Scalars will print like 1-item vectors and vectors print like 1-row matrices.
        # Higher-rank arrays print like matrices spaced out vertically.
        # Start by finding the str representation of each element of the array and then
        # lay everything out, framing with nice characters like └┴┘├┼┤┌┬┐─│.
        rank = len(self.shape)
        if not rank:
            return str(APLArray([1, 1], [self.data]))
        elif rank == 1:
            return str(APLArray([1]+self.shape, self.data))
        else:
            # Find how many rows and columns each element needs.
            strs = []
            trailing_size = self.shape[-1]
            widths = [0 for _ in range(trailing_size)]
            height = 0
            for i, d in enumerate(self.data):
                s = str(d)
                height = max(height, 1+s.count("\n"))
                widths[i%trailing_size] = max(widths[i%trailing_size], 1+(len(s)-height-1)//height)
                strs.append(s)

            # Build the sub-matrices with these dimensions.
            matrix_size = self.shape[-2]*self.shape[-1]
            n_matrices = math.prod(self.shape)//matrix_size
            matrices = []
            for i in range(n_matrices):
                m = _frame_matrix(strs[i*matrix_size:(i+1)*matrix_size], widths, height)
                matrices.append(m)

            # Concatenate all the matrices and leave the appropriate newlines in between.
            newline_offsets = [math.prod(self.shape[-i-1:-2]) for i in range(rank-2)]
            string = ""
            for i, m in enumerate(matrices):
                string += sum(i!=0 and 0 == i%l for l in newline_offsets)*"\n "
                string += m + " "
            return string

    __repr__ = __str__

    def __eq__(self, other):
        return (
            isinstance(other, APLArray) and
            self.shape == other.shape and
            self.data == other.data
        )

def _simple_scalar_str(s):
    if isinstance(s, complex):
        return "J".join(map(_simple_scalar_str, [s.real, s.imag]))
    # Non-complex numeric type:
    elif s < 0:
        return f"¯{-s}"
    elif int(s) == s:
        return str(int(s))
    else:
        return str(s)

def _frame_matrix(strs, widths, height):
    """Frames the values of a matrix with └┴┘├┼┤┌┬┐─│.

    `height` gives the vertical space each matrix element should occupy.
    `widths` gives the horizontal each column in the matrix should occupy.
    The matrix has as many columns as `widths` has elements and the number
        of rows is `len(strs)/len(widths)`.
    """

    ncols = len(widths)
    nrows = len(strs)//ncols

    print(strs)
    print(widths)
    print(height)
    print("@"*30)
    boxes = []
    for i, s in enumerate(strs):
        boxes.append(_box(s, widths[i%ncols], height))

    rows = []
    for i in range(nrows):
        row = _block_join(" │ ", boxes[i*len(widths):(i+1)*len(widths)])
        print(row.__repr__())
        row = _block_prepend(row, "│")
        row = _block_append(row, "│")
        rows.append(row)
    print("#"*30)

    # Get a matrix reference line to build the top, intermediate and bottom lines.
    ref_line = rows[0].split("\n")[0]
    top = "┌"
    for char in ref_line[1:-1]:
        top += "┬" if char == "│" else "─"
    top += "┐"
    intermediate = "├" + top[1:-1].replace("┬", "┼") + "┤"
    bot = "└" + top[1:-1].replace("┬", "┴") + "┘"

    # Put everything together.
    lines = [top]
    for row in rows:
        lines.extend(row.split("\n"))
        lines.append(intermediate)
    lines[-1] = bot
    return "\n".join(lines)

def _box(s, w, h):
    """Make s have h lines, each of length w, with s on the top-left corner."""

    lines = s.split("\n")
    lines = list(map(lambda l: l + (w-len(l))*" ", lines))
    lines = lines + [" "*w]*(h-len(lines))
    return "\n".join(lines)

def _block_join(sep, blocks):
    """Join a sequence of appropriately sized blocks with the given separator."""

    if not blocks:
        return ""
    r = blocks[0]
    for b in blocks[1:]:
        r = _block_concat(_block_append(r, sep), b)
    return r

def _block_concat(left, right):
    """Concatenate two blocks of lines of appropriate shapes."""

    return "\n".join(
        l+r for l, r in zip(left.split("\n"), right.split("\n"))
    )

def _block_prepend(string, val):
    """Prepends val to each line of string."""
    return "\n".join(
        map(lambda l: val+l, string.split("\n"))
    )

def _block_append(string, val):
    """Append val to each line of string."""
    return "\n".join(
        map(lambda l: l+val, string.split("\n"))
    )

s = lambda v: APLArray([], v)
m1 = APLArray([2,2],[s(1),s(2),s(3),s(4)])
m2 = APLArray([2,3], [s(0),s(-34),s(0.001),s(complex(3,0.2)),s(0),s(0)])

print(m2)
print(APLArray([2,2],[m1,m1,m1,m2]))