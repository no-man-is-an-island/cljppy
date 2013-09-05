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
from threading import Thread


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


def parallelise(*arity_zero_funcs):
    """
    Will parallelise calls to any number of zero-arity funcs,
    terminating when they have all completed. Since python doesn't *really*
    have parallelisation, only concurrency, this should be used for
    functions which block on non-python processes (e.g. shell commands)
    """
    # TODO: Check for exceptions
    threads = [Thread(target=f) for f in arity_zero_funcs]
    doseq(Thread.start, threads)
    doseq(Thread.join, threads)


def memoize(f):
    """
    Takes a *pure* function and returns a memoized version of the function
    that keeps a cache of the mapping from arguments
    to results and, when calls with the same arguments are repeated often, has
    higher performance at the expense of higher memory use.
    """
    cache = {}

    def f_star(*args):
        if args in cache:
            return cache[args]
        else:
            result = f(*args)
            cache[args] = result
            return result

    return f_star


def comp(*fs):
    """
    Takes a set of functions and returns a fn that is the composition
    of those fns. The returned fn takes a variable number of args,
    applies the rightmost of fns to the args, the next
    fn (right-to-left) to the result, etc.
    """
    from cljppy.sequence import reverse, but_last, last

    def _function(*args, **kwargs):
        return reduce(
            lambda acc, f: f(acc),
            reverse(but_last(fs)),
            last(fs)(*args, **kwargs))

    return _function