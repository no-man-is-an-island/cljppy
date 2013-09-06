from threading import Thread
from cljppy.sequence import reverse, but_last, last, doseq, empty, map
from cljppy.core import identity


def comp(*fs):
    """
    Takes a set of functions and returns a fn that is the composition
    of those fns. The returned fn takes a variable number of args,
    applies the rightmost of fns to the args, the next
    fn (right-to-left) to the result, etc.
    """
    if empty(fs):
        return identity

    def _function(*args, **kwargs):
        return reduce(
            lambda acc, f: f(acc),
            reverse(but_last(fs)),
            last(fs)(*args, **kwargs))

    return _function


def juxt(*fs):
    """
    Takes a set of functions and returns a fn that is the juxtaposition
    of those fns. The returned fn takes a variable number of args, and
    returns a vector containing the result of applying each fn to the
    args (left-to-right).
    ((juxt a b c) x) => [(a x) (b x) (c x)]
    """
    def _juxt(*args):
        return list(map(lambda f: f(*args), fs))

    return _juxt


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

