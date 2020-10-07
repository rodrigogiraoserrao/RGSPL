"""
Module that implements APL's monadic operators.
"""

import math

from arraymodel import APLArray

def commute(*, aalpha):
    """Define the monadic commute ⍨ operator.

    Monadic case:
        f⍨ ⍵
    ⍵ f ⍵
    Dyadic case:
        ⍺ f⍨ ⍵
    ⍵ f ⍺
    """

    def derived(*, alpha=None, omega):
        alpha = omega if alpha is None else alpha
        return aalpha(alpha=omega, omega=alpha)
    return derived

def diaeresis(*, aalpha):
    """Define the monadic diaeresis ¨ operator.

    Monadic case:
        f¨ x y z
    (f x) (f y) (f z)
    Dyadic case:
        ⍺ f¨ x y z
    (⍺ f x) (⍺ f y) (⍺ f z)
        x y z f¨ ⍵
    (x f ⍵) (y f ⍵) (z f ⍵)
        a b c f¨ x y z
    (a f x) (b f y) (c f z)
    """

    def derived(*, alpha=None, omega):
        if alpha:
            if alpha.shape and omega.shape:
                if len(alpha.shape) != len(omega.shape):
                    raise ValueError("Mismatched ranks of left and right arguments.")
                elif alpha.shape and omega.shape and alpha.shape != omega.shape:
                    raise IndexError("Left and right arguments must have the same dimensions.")
            shape = alpha.shape or omega.shape
        else:
            shape = omega.shape
        
        l = math.prod(shape)
        omegas = omega.data if omega.shape else l*[omega]
        alphas = l*[None] if alpha is None else (
            alpha.data if alpha.shape else l*[alpha]
        )
        data = [aalpha(omega=o, alpha=a) for o, a in zip(omegas, alphas)]
        if not shape:
            data = data[0]
        return APLArray(shape, data)
    return derived
