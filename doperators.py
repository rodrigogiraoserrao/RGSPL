"""
Module that implements APL's dyadic operators.
"""

def jot(*, aalpha, oomega):
    """Define the dyadic jot ∘ operator.

    Monadic case:
        f∘g ⍵
    f g ⍵
    Dyadic case:
        ⍺ f∘g ⍵
    ⍺ f g ⍵
    """

    def derived(*, alpha=None, omega):
        return aalpha(alpha=alpha, omega=oomega(omega=omega))
    return derived
