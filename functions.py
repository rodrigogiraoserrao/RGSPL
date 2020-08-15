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
    def pervasive_func(*, alpha=None, omega):
        if not isinstance(omega, list) and not isinstance(alpha, list):
            return func(alpha=alpha, omega=omega)
        elif isinstance(omega, list) and isinstance(alpha, list):
            if len(omega) != len(alpha):
                raise IndexError("Cannot pervade with mismatched lengths.")
            return [pervasive_func(omega=w, alpha=a) for a, w in zip(alpha, omega)]
        elif isinstance(omega, list):
            return [pervasive_func(alpha=alpha, omega=w) for w in omega]
        else:
            return [pervasive_func(alpha=a, omega=omega) for a in alpha]

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

@pervade
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

@pervade
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

    return [int(omega[i] not in omega[:i]) for i in range(len(omega))]

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

def _nested_prepend(value, array):
    """Takes a value and prepends it to every sublist of the array."""

    if isinstance(array, list) and not isinstance(array[0], list):
        return [value] + array
    else:
        return [_nested_prepend(value, sub) for sub in array]

def iota(*, alpha=None, omega):
    """Define monadic index generator and dyadic index of.

    Monadic case:
        ⍳ 4
    0 1 2 3
    Dyadic case:
        6 5 32 4 ⍳ 32
    2
    """

    if alpha is not None:
        if not isinstance(alpha, list):
            raise TypeError(
                f"Cannot find index of elements in {type(alpha)} left argument."
            )
        if not isinstance(omega, list):
            return alpha.index(omega) if omega in alpha else len(alpha)
        else:
            return [alpha.index(w) if w in alpha else len(alpha) for w in omega]
    else:
        if isinstance(omega, int):
            return list(range(omega))
        elif isinstance(omega, list) and len(omega) == 1:
            return list(range(omega[0]))
        elif isinstance(omega, list) and len(omega) == 2:
            return [[[i, j] for j in range(omega[1])] for i in range(omega[0])]
        elif isinstance(omega, list) and len(omega) > 2:
            ret = iota(alpha=None, omega=omega[1:])
            return [_nested_prepend(i, ret) for i in range(omega[0])]
        else:
            raise TypeError(f"Cannot generate indices from {type(omega)}.")
