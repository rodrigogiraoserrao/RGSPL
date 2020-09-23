"""
Module that implements APL's monadic operators.
"""

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
        ⍺ f x y z
    (⍺ f x) (⍺ f y) (⍺ f z)
        x y z f ⍵
    (x f ⍵) (y f ⍵) (z f ⍵)
        a b c f x y z
    (a f x) (b f y) (c f z)
    """

    def derived(*, alpha=None, omega):
        if not isinstance(alpha, list) and not isinstance(omega, list):
            return aalpha(alpha=alpha, omega=omega)
        elif isinstance(alpha, list) and isinstance(omega, list):
            if len(alpha) != len(omega):
                raise IndexError(f"Left and right arguments must have the same length.")
            else:
                return [aalpha(alpha=a, omega=w) for a, w in zip(alpha, omega)]
        elif isinstance(omega, list):
            return [aalpha(alpha=alpha, omega=w) for w in omega]
        else:
            return [aalpha(alpha=a, omega=omega) for a in alpha]
    return derived
