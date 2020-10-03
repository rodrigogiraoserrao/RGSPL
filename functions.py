"""
Module that implements APL's primitive functions.

cf. https://www.jsoftware.com/papers/satn40.htm for complex GCD.
cf. https://www.jsoftware.com/papers/eem/complexfloor.htm for complex floor.
"""

import functools
import math

from arraymodel import APLArray

def pervade(func):
    """Decorator to define function pervasion into simple scalars."""

    @functools.wraps(func)
    def pervasive_func(*, alpha=None, omega):
        # Start by checking if alpha is None
        if alpha is None:
            if omega.shape:
                data = [
                    pervasive_func(omega=w, alpha=alpha) for w in omega.data
                ]
            elif isinstance(omega.data, APLArray):
                data = pervasive_func(omega=omega.data, alpha=alpha)
            else:
                data = func(omega=omega.data, alpha=alpha)
        # Dyadic case from now on
        elif alpha.shape and omega.shape:
            if alpha.shape != omega.shape:
                raise IndexError("Mismatched left and right shapes.")
            data = [
                pervasive_func(omega=w, alpha=a) for w, a in zip(omega.data, alpha.data)
            ]
        elif alpha.shape:
            w = omega.data if isinstance(omega.data, APLArray) else omega
            data = [pervasive_func(omega=w, alpha=a) for a in alpha.data]
        elif omega.shape:
            a = alpha.data if isinstance(alpha.data, APLArray) else alpha
            data = [pervasive_func(omega=w, alpha=a) for w in omega.data]
        # Both alpha and omega are simple scalars
        elif not isinstance(alpha.data, APLArray) and not isinstance(omega.data, APLArray):
            data = func(omega=omega.data, alpha=alpha.data)
        else:
            a = alpha.data if isinstance(alpha.data, APLArray) else alpha
            w = omega.data if isinstance(omega.data, APLArray) else omega
            data = pervasive_func(omega=w, alpha=a)

        shape = getattr(alpha, "shape", None) or omega.shape
        return APLArray(shape, data)

    return pervasive_func

@pervade
def plus(*, alpha=None, omega):
    """Define monadic complex conjugate and binary addition.

    Monadic case:
        + 1 ¯4 5J6
    1 ¯4 5J¯6
    Dyadic case:
        1 2 3 + ¯1 5 0J1
    0 7 3J1
    """

    if alpha is None:
        return omega.conjugate()
    else:
        return alpha + omega

@pervade
def minus(*, alpha=None, omega):
    """Define monadic symmetric numbers and dyadic subtraction.

    Monadic case:
        - 1 2 ¯3 4J1
    ¯1 ¯2 3 ¯4J¯1
    Dyadic case:
        1 - 3J0.5
    ¯2J¯0.5
    """

    if alpha is None:
        alpha = 0
    return alpha - omega

@pervade
def times(*, alpha=None, omega):
    """Define monadic sign and dyadic multiplication.

    Monadic case:
        × 1 2 0 ¯6
    1 1 0 ¯1
    Dyadic case:
        1 2 3 × 0 3 5
    0 6 15
    """

    if alpha is None:
        if not omega:
            return 0
        else:
            div = omega/abs(omega)
            if not isinstance(omega, complex):
                div = round(div)
            return div
    else:
        return alpha*omega

@pervade
def divide(*, alpha=None, omega):
    """Define monadic reciprocal and dyadic division.

    Monadic case:
        ÷ 1 ¯2 5J10
    1 ¯0.5 0.04J¯0.08
    Dyadic case:
        4 ÷ 3
    1.33333333
    """

    if alpha is None:
        alpha = 1
    return alpha/omega

@pervade
def ceiling(*, alpha=None, omega):
    """Define monadic ceiling and dyadic max.

    Monadic case:
        ⌈ 0.0 1.1 ¯2.3
    0 2 ¯2
    Monadic complex ceiling not implemented yet.
    Dyadic case:
        ¯2 ⌈ 4
    4
    """

    if alpha is None:
        if isinstance(alpha, complex):
            raise NotImplementedError("Complex ceiling not implemented yet.")
        return math.ceil(omega)
    else:
        return max(alpha, omega)

@pervade
def floor(*, alpha=None, omega):
    """Define monadic floor and dyadic min.

    Monadic case:
        ⌊ 0.0 1.1 ¯2.3
    0 1 ¯3
    Monadic complex floor not implemented yet.
    Dyadic case:
        ¯2 ⌊ 4
    ¯2
    """

    if alpha is None:
        if isinstance(alpha, complex):
            raise NotImplementedError("Complex floor not implemented yet.")
        return math.floor(omega)
    else:
        return min(alpha, omega)

def right_tack(*, alpha=None, omega):
    """Define monadic same and dyadic right.

    Monadic case:
        ⊢ 3
    3
    Dyadic case:
        1 2 3 ⊢ 4 5 6
    4 5 6
    """

    return omega

def left_tack(*, alpha=None, omega):
    """Define monadic same and dyadic left.

    Monadic case:
        ⊣ 3
    3
    Dyadic case:
        1 2 3 ⊣ 4 5 6
    1 2 3
    """

    return alpha if alpha is not None else omega

@pervade
def less(*, alpha=None, omega):
    """Define dyadic comparison function less than.

    Dyadic case:
        3 < 2 3 4
    0 0 1
    """

    return int(alpha < omega)

@pervade
def lesseq(*, alpha=None, omega):
    """Define dyadic comparison function less than or equal to.

    Dyadic case:
        3 ≤ 2 3 4
    0 1 1
    """

    return int(alpha <= omega)

@pervade
def eq(*, alpha=None, omega):
    """Define dyadic comparison function equal to.

    Dyadic case:
        3 = 2 3 4
    0 1 0
    """

    return int(alpha == omega)

@pervade
def greatereq(*, alpha=None, omega):
    """Define dyadic comparison function greater than or equal to.

    Dyadic case:
        3 ≥ 2 3 4
    1 1 0
    """

    return int(alpha >= omega)

@pervade
def greater(*, alpha=None, omega):
    """Define dyadic comparison function greater than.

    Dyadic case:
        3 > 2 3 4
    1 0 0
    """

    return int(alpha > omega)

@pervade
def _neq(*, alpha=None, omega):
    """Define dyadic comparison function not equal to.

    Dyadic case:
        3 ≠ 2 3 4
    1 0 1
    """

    return int(alpha != omega)

def _unique_mask(*, alpha=None, omega):
    """Define monadic unique mask.

    Monadic case:
        ≠ 1 1 2 2 3 3 1
    1 0 1 0 1 0 0
    """

    if not omega.shape:
        return APLArray([], 1)

    # find how many elements each major cell has and split the data in major cells
    mcl = int(math.prod(omega.shape)/omega.shape[0])
    major_cells = [omega.data[i*mcl:(i+1)*mcl] for i in range(omega.shape[0])]
    return APLArray(
        [omega.shape[0]],
        [int(major_cell not in major_cells[:i]) for i, major_cell in enumerate(major_cells)]
    )

def neq(*, alpha=None, omega):
    """Define monadic unique mask and dyadic not equal to.

    Monadic case:
        ≠ 1 1 2 2 3 3 1
    1 0 1 0 1 0 0
    Dyadic case:
        3 ≠ 2 3 4
    1 0 1
    """

    if alpha is None:
        return _unique_mask(alpha=alpha, omega=omega)
    else:
        return _neq(alpha=alpha, omega=omega)

@pervade
def _not(*, alpha=None, omega):
    """Define monadic not.

    Monadic case:
        ~ 1 0 1 0 0 1 0 0
    0 1 0 1 1 0 1 1
    """

    return int(not omega)

def lshoe(*, alpha=None, omega):
    """Define monadic and dyadic left shoe.

    Monadic case:
        ⊂ 1 2 3
    (1 2 3)
        ⊂ 1
    1
    Dyadic case:
        NotImplemented
    """

    if alpha is None:
        if (not omega.shape) and (not isinstance(omega.data, APLArray)):
            return omega
        else:
            return APLArray([], omega)
    else:
        raise NotImplementedError("Partitioned Enclose not implemented yet.")

def _without(*, alpha=None, omega):
    """Define dyadic without.

    Dyadic case:
        3 1 4 1 5 ~ 1 5
    3 4
    """

    if (r := len(alpha.shape)) > 1:
        raise ValueError(f"Cannot use Without with array of rank {r}")

    if omega.shape == []:
        haystack = [omega.data] if isinstance(omega.data, APLArray) else [omega]
    else:
        haystack = omega.data
    if alpha.shape == []:
        needles = [alpha.data] if isinstance(alpha.data, APLArray) else [alpha]
    else:
        needles = alpha.data
    newdata = [needle for needle in needles if needle not in haystack]
    return APLArray([len(newdata)], newdata)

def without(*, alpha=None, omega):
    """Define monadic not and dyadic without.

    Monadic case:
        ~ 1 0 1 0 0 1 0 0
    0 1 0 1 1 0 1 1
    Dyadic case:
        3 1 4 1 5 ~ 1 5
    3 4
    """

    if alpha is None:
        return _not(alpha=alpha, omega=omega)
    else:
        return _without(alpha=alpha, omega=omega)

def _decode(radices, n):
    """Decode n into the repeated radices given.

    Dyadic case (10000 seconds is 2h 46min 40s):
        24 60 60 ⊤ 10000
    2 46 40
    """

    bs = []
    for m in radices[::-1]:
        n, b = divmod(n, m)
        bs.append(b)
    return bs[::-1]

def _index_generator(*, alpha=None, omega):
    """Define monadic Index Generator.

    Monadic case:
        ⍳ 4
    0 1 2 3
    """

    d = omega.data
    if isinstance(d, int):
        shape = [d]
    elif isinstance(d, list):
        shape = [sub.data for sub in d]

    if any(not isinstance(dim, int) for dim in shape):
        raise TypeError(f"Cannot generate indices with non-integers {shape}")
    elif any(dim < 0 for dim in shape):
        raise ValueError("Cannot generate indices with negative integers")

    decoded = map(lambda n: _decode(shape, n), range(math.prod(shape)))
    if (l := len(shape)) == 1:
        data = [APLArray([], d[0]) for d in decoded]
    else:
        data = [APLArray([l], d) for d in decoded]
    return APLArray(shape, data)

def iota(*, alpha=None, omega):
    """Define monadic index generator and dyadic index of.

    Monadic case:
        ⍳ 4
    0 1 2 3
    Dyadic case:
        6 5 32 4 ⍳ 32
    2
    """

    if alpha is None:
        return _index_generator(alpha=alpha, omega=omega)
    else:
        raise NotImplementedError("Index Of not implemented yet.")
