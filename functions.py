"""
Module that implements APL's primitive functions.

cf. https://www.jsoftware.com/papers/satn40.htm for complex GCD.
cf. https://www.jsoftware.com/papers/eem/complexfloor.htm for complex floor.
"""

import functools
import math

from arraymodel import APLArray, S

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
            elif isinstance(omega.data[0], APLArray):
                data = [pervasive_func(omega=omega.data[0], alpha=alpha)]
            else:
                data = [func(omega=omega.data[0], alpha=alpha)]
        # Dyadic case from now on
        elif alpha.shape and omega.shape:
            if alpha.shape != omega.shape:
                raise IndexError("Mismatched left and right shapes.")
            data = [
                pervasive_func(omega=w, alpha=a) for w, a in zip(omega.data, alpha.data)
            ]
        elif alpha.shape:
            w = omega if omega.is_simple_scalar() else omega.data[0]
            data = [pervasive_func(omega=w, alpha=a) for a in alpha.data]
        elif omega.shape:
            a = alpha if alpha.is_simple_scalar() else alpha.data[0]
            data = [pervasive_func(omega=w, alpha=a) for w in omega.data]
        # Both alpha and omega are simple scalars
        elif alpha.is_simple_scalar() and omega.is_simple_scalar():
            data = [func(omega=omega.data[0], alpha=alpha.data[0])]
        else:
            a = alpha if alpha.is_simple_scalar() else alpha.data[0]
            w = omega if omega.is_simple_scalar() else omega.data[0]
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

    majors = omega.major_cells()
    data = [
        APLArray([], [int(major_cell not in majors.data[:i])])
        for i, major_cell in enumerate(majors.data)
    ]
    return APLArray([len(data)], data)

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
        if omega.is_simple_scalar():
            return omega
        else:
            return APLArray([], [omega])
    else:
        raise NotImplementedError("Partitioned Enclose not implemented yet.")

@pervade
def _not(*, alpha=None, omega):
    """Define monadic not.

    Monadic case:
        ~ 1 0 1 0 0 1 0 0
    0 1 0 1 1 0 1 1
    """

    return int(not omega)

def _without(*, alpha=None, omega):
    """Define dyadic without.

    Dyadic case:
        3 1 4 1 5 ~ 1 5
    3 4
        (3 2⍴⍳6) ~ 0 1
    2 3
    4 5
    """

    alpha_majors = alpha.major_cells()
    needle_rank = len(alpha.shape) - 1
    if needle_rank > len(omega.shape):
        raise ValueError(f"Right argument to ~ needs rank at least {needle_rank}.")
    # Get a list with the arrays that we wish to exclude from the left.
    haystack = omega.n_cells(needle_rank).data

    newdata = []
    count = 0
    for major in alpha_majors.data:
        if major not in haystack:
            if major.is_scalar():
                newdata.append(major)
            else:
                newdata += major.data
            count += 1
    newshape = [count] + alpha.shape[1:]
    return APLArray(newshape, newdata)

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

def _encode(radices, n):
    """Encode n into the radices given.

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

    if (r := len(omega.shape)) > 1:
        raise ValueError(f"Index generator did not expect array of rank {r}.")

    if omega.is_scalar() and isinstance(omega.data[0], int):
        shape = [omega.data[0]]
    else:
        # If omega is not a scalar, then we want the integers that compose the vector.
        shape = [elem.data[0] for elem in omega.data]

    # Check the argument to index generator is only non-negative integers.
    if any(not isinstance(dim, int) for dim in shape):
        raise TypeError(f"Cannot generate indices with non-integers {shape}.")
    elif any(dim < 0 for dim in shape):
        raise ValueError("Cannot generate indices with negative integers.")

    decoded = map(lambda n: _encode(shape, n), range(math.prod(shape)))
    if omega.is_scalar():
        data = [S(d[0]) for d in decoded]
    else:
        r = len(shape)
        data = [APLArray([r], list(map(S, d))) for d in decoded]
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

def rho(*, alpha=None, omega):
    """Define monadic shape and dyadic reshape.

    Monadic case:
        ⍴ ⍳2 3
    2 3
    Dyadic case:
        3⍴⊂1 2
    (1 2)(1 2)(1 2)
    """

    if alpha is None:
        shape = [len(omega.shape)]
        data = [S(i) for i in omega.shape]
        return APLArray(shape, data)
    else:
        rank = len(alpha.shape)
        if rank > 1:
            raise ValueError(f"Left argument of reshape cannot have rank {rank}.")
        
        if alpha.is_scalar():
            shape = [alpha.data[0]]
        else:
            shape = [d.data[0] for d in alpha.data]

        if not all(isinstance(i, int) for i in shape):
            raise TypeError("Left argument of reshape expects integers.")

        data_from = omega.data if len(omega.shape) > 0 else [omega]
        # Extend the data roughly if needed, then truncate if needed.
        data = data_from*(math.ceil(math.prod(shape)/len(data_from)))
        data = data[:math.prod(shape)]
        return APLArray(shape, data)
