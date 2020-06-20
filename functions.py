"""
Module that implements APL's primitive functions.

cf. https://www.jsoftware.com/papers/satn40.htm for complex GCD.
cf. https://www.jsoftware.com/papers/eem/complexfloor.htm for complex floor.
"""

import functools
import math

def pervade(func):
    """Decorator to define function pervasion into simple scalars."""

    @functools.wraps(func)
    def pervasive_func(w, a=None):
        if not isinstance(w, list) and not isinstance(a, list):
            return func(w, a)
        elif isinstance(w, list) and isinstance(a, list):
            if len(w) != len(a):
                raise IndexError("Cannot pervade with mismatched lengths.")
            return [pervasive_func(w_, a_) for w_, a_ in zip(w, a)]
        elif isinstance(w, list):
            return [pervasive_func(w_, a) for w_ in w]
        else:
            return [pervasive_func(w, a_) for a_ in a]

    return pervasive_func

@pervade
def plus(w, a=None):
    """Define monadic complex conjugate and binary addition.

    Monadic case:
        + 1 ¯4 5J6
    1 ¯4 5J¯6
    Dyadic case:
        1 2 3 + ¯1 5 0J1
    0 7 3J1
    """

    if a is None:
        return w.conjugate()
    else:
        return a + w

@pervade
def minus(w, a=0):
    """Define monadic symmetric numbers and dyadic subtraction.

    Monadic case:
        - 1 2 ¯3 4J1
    ¯1 ¯2 3 ¯4J¯1
    Dyadic case:
        1 - 3J0.5
    ¯2J¯0.5
    """

    return a - w

@pervade
def times(w, a=None):
    """Define monadic sign and dyadic multiplication.

    Monadic case:
        × 1 2 0 ¯6
    1 1 0 ¯1
    Dyadic case:
        1 2 3 × 0 3 5
    0 6 15
    """

    if a is None:
        if not w:
            return 0
        else:
            div = w/abs(w)
            if not isinstance(w, complex):
                div = round(div)
            return div
    else:
        return a*w

@pervade
def divide(w, a=1):
    """Define monadic reciprocal and dyadic division.

    Monadic case:
        ÷ 1 ¯2 5J10
    1 ¯0.5 0.04J¯0.08
    Dyadic case:
        4 ÷ 3
    1.33333333
    """

    return a/w

@pervade
def ceiling(w, a=None):
    """Define monadic ceiling and dyadic max.

    Monadic case:
        ⌈ 0.0 1.1 ¯2.3
    0 2 ¯2
    Monadic complex ceiling not implemented yet.
    Dyadic case:
        ¯2 ⌈ 4
    4
    """

    if a is None:
        if isinstance(a, complex):
            raise NotImplementedError("Complex ceiling not implemented yet.")
        return math.ceil(w)
    else:
        return max(a, w)

@pervade
def floor(w, a=None):
    """Define monadic floor and dyadic min.

    Monadic case:
        ⌊ 0.0 1.1 ¯2.3
    0 1 ¯3
    Monadic complex floor not implemented yet.
    Dyadic case:
        ¯2 ⌊ 4
    ¯2
    """

    if a is None:
        if isinstance(a, complex):
            raise NotImplementedError("Complex floor not implemented yet.")
        return math.floor(w)
    else:
        return min(a, w)
