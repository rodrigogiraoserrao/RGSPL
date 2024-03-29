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

def dyadic(op):
    """Decorator that ensures that the corresponding APL primitive is called dyadically."""

    def inner(func):
        @functools.wraps(func)
        def wrapped(*, alpha=None, omega):

            if alpha is None:
                raise SyntaxError(f"{op} is a dyadic function.")
            return func(alpha=alpha, omega=omega)

        return wrapped
    return inner

TYPES = {
    "boolean": lambda x: x in [0, 1],
    int: lambda x: isinstance(x, int),
}

def arg_types(op, alpha_type=None, omega_type=None):
    """Decorator that ensures a scalar APL function receives args with given types."""

    def inner(func):
        @functools.wraps(func)
        def wrapped(*, alpha=None, omega):
            if (check := TYPES.get(alpha_type)) is not None:
                if not check(alpha):
                    raise TypeError(f"{op} expected a left argument of type {alpha_type}.")
            if (check := TYPES.get(omega_type)) is not None:
                if not check(omega):
                    raise TypeError(f"{op} expected a right argument of type {omega_type}.")
            return func(alpha=alpha, omega=omega)

        return wrapped
    return inner

def boolean_function(op):
    """Decorator that ensures a Boolean function gets passed Boolean arguments."""
    return arg_types(op, "boolean", "boolean")

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
@boolean_function("∧")
@dyadic("∧")
def and_(*, alpha=None, omega):
    """Define dyadic Boolean and.

    Dyadic case:
        0 0 1 1 ∧ 0 1 0 1
    0 0 0 1
    """

    return alpha and omega

@pervade
@boolean_function("⍲")
@dyadic("⍲")
def nand(*, alpha=None, omega):
    """Define dyadic Boolean nand function.

    Dyadic case:
        0 0 1 1 ⍲ 0 1 0 1
    1 1 1 0
    """

    return 1 - (alpha and omega)

@pervade
@boolean_function("∨")
@dyadic("∨")
def or_(*, alpha=None, omega):
    """Define dyadic Boolean or function.

    Dyadic case:
        0 0 1 1 ∨ 0 1 0 1
    0 1 1 1
    """

    return alpha or omega

@pervade
@boolean_function("⍱")
@dyadic("⍱")
def nor(*, alpha=None, omega):
    """Define dyadic Boolean nor function.

    Dyadic case:
        0 0 1 1 ⍱ 0 1 0 1
    1 0 0 0
    """

    return 1 - (alpha or omega)

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

def _decode(alpha, omega):
    """Helper function that decodes one APLArray w.r.t. to another.

    Notice that this goes against the _encode helper function, that
    _does not_ deal with APLArray objects.
    """

    acc = 0
    acc_prod = 1
    alphas = [a.data[0] for a in alpha.data]
    omegas = [o.data[0] for o in omega.data]
    for a, o in zip(alphas[::-1], omegas[::-1]):
        acc += acc_prod * o
        acc_prod *= a
    return S(acc)

@dyadic("⊥")
def decode(*, alpha=None, omega):
    """Define dyadic decode.

    Dyadic case:
        2 ⊥ 1 1 0 1
    13
        24 60 60 ⊥ 2 46 40
    10000
    """

    # Compute the final shape now, then promote omega for ease of computation.
    final_shape = alpha.shape[:-1] + omega.shape[1:]
    omega = omega.at_least_vector()

    # Ensure alpha has the correct shape:
    if alpha.is_simple_scalar() or alpha.shape == [1]:
        alpha = rho(alpha=S(omega.shape[0]), omega=alpha)

    # Ensure omega has the correct leading dimension:
    if omega.shape[0] != alpha.shape[-1]:
        if omega.shape[0] != 1:
            raise IndexError("Trailing dimension of ⍺ should match leading dimension of ⍵ in ⍺⊥⍵.")
        target_shape_values = [S(v) for v in [alpha.shape[-1]]+omega.shape[1:]]
        target_shape = APLArray([len(omega.shape)], target_shape_values)
        omega = rho(alpha=target_shape, omega=omega)

    dist = math.prod(omega.shape[1:])
    omega_first_axis_enclosure = APLArray(
        omega.shape[1:],
        [APLArray([omega.shape[0]], omega.data[i::dist]) for i in range(dist)]
    )
    # Pair each 1-cell of alpha with each element in the first axis enclosure of omega.
    data = [_decode(a, o) for a in alpha.n_cells(1).data for o in omega_first_axis_enclosure.data]
    # Check if we should return a container array or just a single simple scalar.
    return APLArray(final_shape, data) if final_shape else data[0]

def _encode(radices, n):
    """Helper function to the encode ⊤ primitive.

    Takes a list of radices and a simple scalar n.
    (Notice that `radices` and `n` are _not_ APLArray objects)

    E.g. (10000 seconds is 2h 46min 40s):
        24 60 60 ⊤ 10000
    2 46 40
    """

    n = n % (math.prod(radices) if 0 not in radices else n + 1)
    bs = []
    for m in radices[::-1]:
        n, b = divmod(n, m) if m != 0 else (0, n)
        bs.append(b)
    return bs[::-1]

@dyadic("⊤")
def encode(*, alpha=None, omega):
    """Define dyadic encode.

    Dyadic case:
        2 3 4 ⊤ 23 24
    1 0
    2 0
    3 0

    Notice that alpha has the radices along its first dimension.
    Therefore, the first axis enclosure of alpha gives vectors with the radices.
    The final result has the encodings also along the first axis,
    so the first axis enclosure of the result is easy to relate to the first axis
    enclosure of alpha and the original omega.
    """

    # Compute the resulting shape now and promote alpha for ease of calculations.
    result_shape = alpha.shape + omega.shape
    alpha = alpha.at_least_vector()
    result_data = [0]*math.prod(result_shape)
    # Radices come from alpha.shape[i::dist] (~ the first axis enclosure of alpha).
    dist = math.prod(alpha.shape[1:])
    # Resulting vectors go to result_data[j::rdist] (~ the first axis enclosure of the result).
    rdist = math.prod(result_shape[1:])
    for i in range(dist):
        radices = [s.data[0] for s in alpha.data[i::dist]]
        for j, s in enumerate(omega.at_least_vector().data):
            result_data[i*math.prod(omega.shape)+j::rdist] = map(S, _encode(radices, s.data[0]))

    return APLArray(result_shape, result_data) if result_shape else result_data[0]
