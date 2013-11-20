#-------------------------------------------------------------------------------
# Name:        cljppy.core
#
# Purpose:     'Core' functions that might be needed anywhere (helps us
#              avoid cyclic dependencies
#
# Author:      David Williams
#
# Created:     27/07/2013
# Copyright:   (c) David Williams 2013
#-------------------------------------------------------------------------------
from itertools import chain


def identity(x):
    """
    The identity function.
    e.g. filter(identity, [1, 2, None, 3]) -> [1,2,3]
    """
    return x


def constantly(x):
    """
    Returns a function that takes any number of arguments and returns x
    """

    def _function(*args):
        return x

    return _function


def plus(*args):
    """
    Multiargument addition - mainly for testing during development.
    Returns 0 (identity) when sero args passed.. SLOW AS HELL
    e.g.
    reduce(plus, [1,2,3]) -> 6
    apply(plus, [1,2,3]) -> 6
    """
    if len(args) == 0:
        return 0
    else:
        return reduce(lambda x, y: x + y, args)


def mult(*args):
    """
    Multiargument multiplication - mainly for testing during development.
    Returns 1 (identity) when zero args passed. SLOW AS HELL
    """
    if len(args) == 0:
        return 1
    else:
        return reduce(lambda x, y: x * y, args)


def strcat(*args):
    """
    Multi-arity string joining
    """
    return reduce(lambda x, y: str(x) + str(y), args, "")


def even(x):
    """
    Predicate to check if an int is even
    """
    return (x % 2) == 0


def dorun(iterable):
    """
    Evaluates all the values of an iterable, presumably for side-effects.
    Returns None
    """
    for _ in iter(iterable):
        pass


def doall(iterable):
    """
    Evaluates all the values of an iterable, presumably for side-effects.
    Returns a list of the iterable.
    """
    for _ in iter(iterable):
        pass
    return iterable


def doseq(f, iterable):
    """
    Calls f, an arity 1 fn, on each value of an iterable,
    presumably for side-effects. Returns None
    """
    for x in iter(iterable):
        f(x)


def apply(f, args=[]):
    """
    Takes a function f and a sequence of args [x1,x2,..], and returns
    f(x1, x2, ..). Not as good as the multiple arity clojure version :( :(
    """
    return f(*args)


def partial(f, *args):
    """
    Partial application of f to zero or more args
    """

    def _function(*args_inner):
        return f(*chain(args, args_inner))

    return _function


inc = partial(plus, 1)


def group_by(f, coll):
    """
    Returns a map of the elements of coll keyed by the result of
    f on each element. The value at each key will be a vector of the
    corresponding elements, in the order they appeared in coll.
    """
    m = {}

    for x in coll:
        if f(x) in m:
            m[f(x)].append(x)
        else:
            m[f(x)] = [x]

    return m


def every_pred(*ps):
    """
    Takes a set of predicates and returns a function f that returns true if all of its
    composing predicates return a logical true value against all of its arguments, else
    it returns false. Note that f is short-circuiting in that it will stop execution on
    the first argument that triggers a logical false result against the original predicates.
    """
    def _fn(*args):
        for p in ps:
            if not p(*args):
                return False
        return True
    return _fn

def raises(error):
    """
    Returns a function that takes any number of arguments and raises error
    """
    def _fn(*args):
        raise error
    return _fn