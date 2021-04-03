"""
Module to define the array model for APL.
"""

import math

class APLArray:
    """Class to hold APL arrays.

    All arrays have a shape of type list and a list with the data.
    The length of the data attribute is always the product of all
    elements in the shape list, even for scalars (the product
    of an empty list is 1).
    """

    def __init__(self, shape, data):
        self.shape = shape
        self.data = data

    def major_cells(self):
        """Returns an APLArray with the major cells of self."""
        return self.n_cells(len(self.shape)-1)

    def n_cells(self, n):
        """Returns an APLArray with the n-cells of self.

        An array of rank r has r-cells, (r-1)-cells, ..., 0-cells.
        An n-cell is a subarray with n trailing dimensions.

        The result of asking for the n-cells of an array of rank r
        is an APLArray of rank (r-n) with shape equal to the first
        (r-n) elements of the shape of the original array.
        """

        if n == 0:
            return self

        r = len(self.shape)
        if n > r:
            raise ValueError(f"Array of rank {r} does not have {n}-cells.")

        if r == n:
            return S(self)

        result_shape = self.shape[:r-n]
        cell_shape = self.shape[r-n:]
        size = math.prod(cell_shape)
        data = [
            APLArray(cell_shape, self.data[i*size:(i+1)*size])
            for i in range(math.prod(result_shape))
        ]
        return APLArray(result_shape, data)

    def is_scalar(self):
        return not self.shape

    def is_simple_scalar(self):
        return (not self.shape) and (not isinstance(self.data[0], APLArray))

    def at_least_vector(self):
        if self.is_simple_scalar():
            return APLArray([1], [self])
        else:
            return self

    def __str__(self):
        # Print simple scalars nicely.
        if self.is_simple_scalar():
            return _simple_scalar_str(self.data[0])

        # Print simple arrays next.
        if self.shape and all(d.is_simple_scalar() for d in self.data):
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
            return str(APLArray([1, 1], self.data))
        elif rank == 1:
            return str(APLArray([1]+self.shape, self.data))
        else:
            # Find how many rows and columns each element needs.
            strs = []
            trailing_size = self.shape[-1]
            widths = [0 for _ in range(trailing_size)]
            height = 0
            for i, d in enumerate(self.data):
                # If d is a non-simple scalar, print the data instead of the scalar.
                s = str(d)
                s_height = 1+s.count("\n")
                height = max(height, s_height)
                s_width = max(map(len, s.split("\n")))
                widths[i%trailing_size] = max(widths[i%trailing_size], s_width)
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
                string += sum(i!=0 and 0 == i%l for l in newline_offsets)*"\n"
                string += m + " "
            return string[:-1]

    def __repr__(self):
        """Unambiguous representation of an APLArray instance."""
        return f"APLArray({repr(self.shape)}, {repr(self.data)})"

    def __eq__(self, other):
        return (
            isinstance(other, APLArray) and
            self.shape == other.shape and
            self.data == other.data
        )

# Helper method to create APLArray scalars.
S = lambda v: APLArray([], [v])

def _simple_scalar_str(s):
    """String representation of a simple scalar."""

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
    `widths` gives the horizontal space each column in the matrix should occupy.
    The matrix has as many columns as `widths` has elements and the number
        of rows is `len(strs)/len(widths)`.
    """

    ncols = len(widths)
    nrows = len(strs)//ncols
    boxes = []
    for i, s in enumerate(strs):
        boxes.append(_box(s, widths[i%ncols], height))

    rows = []
    for i in range(nrows):
        row = _block_join("│", boxes[i*len(widths):(i+1)*len(widths)])
        row = _block_prepend(row, "│")
        row = _block_append(row, "│")
        rows.append(row)

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
    """Prepend val to each line of string."""
    return "\n".join(
        map(lambda l: val+l, string.split("\n"))
    )

def _block_append(string, val):
    """Append val to each line of string."""
    return "\n".join(
        map(lambda l: l+val, string.split("\n"))
    )
