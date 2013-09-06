#-------------------------------------------------------------------------------
# Name:        cljppy.sequence.generators
#
# Purpose:     Functions that generate (potentially) infinite lazy sequences
#
# Author:      David Williams
#
# Created:     27/07/2013
# Copyright:   (c) David Williams 2013
#-------------------------------------------------------------------------------

import itertools
from cljppy import partial
from cljppy.sequence.LazySequence import LazySequence
from cljppy.sequence.predicates import *
from cljppy.core import *


def repeat(x):
    """
    Returns an infinite lazy sequence of x
    """
    return LazySequence(itertools.repeat(x))

def __cycle(iterable):
    """
    Returns an infinite generator of repetitions of the items in
    the iterable
    """
    if empty(iterable):
        return

    while True:
        for x in iterable:
            yield x

def cycle(iterable):
    """
    Returns an infinite lazy sequence of repetitions of the items in
    the iterable
    """
    return LazySequence(__cycle(iterable))

def __irepeatedly(f, n=None):
    """
    Takes a zero-arity function and returns a lazy sequence of f().
    Optionally takes an integer n to limit the number of calls.
    """
    if n == None:
        while True:
            yield f()
    else:
        for _ in itertools.repeat(None, n):
            yield f()

def repeatedly(f, n = None):
    """
    Takes a zero-arity function and returns a lazy sequence of f().
    Optionally takes an integer n to limit the number of calls.
    """
    return LazySequence(__irepeatedly(f, n))


def __iiterate(f, x, n = None):
    """
    Returns a generator of x, (f x), (f (f x)) etc.
    Optionally takes an integer n to limit the number of calls.
    """
    acc = x
    if n == None:
        while True:
            yield acc
            acc = f(acc)
    else:
        for _ in itertools.repeat(None, n):
            yield acc
            acc = f(acc)

def iterate(f, x, n = None):
    """
    Returns a lazy sequence of x, (f x), (f (f x)) etc.
    Optionally takes an integer n to limit the number of calls.
    """
    return LazySequence(__iiterate(f, x, n))


def __inatural_numbers():
    """
    The natural numbers (starting with 0 of course).
    range is DEFINITELY preferable.. this is just a toy example
    """
    return iterate(partial(plus, 1), 0)

def natural_numbers():
    """
    A lazy sequence of the natural numbers
    """
    return LazySequence(__inatural_numbers())

def __ipowers_of(n):
    """
    Lazily returns all powers of n, starting with 1
    """
    return iterate(partial(mult, n), 1)

def powers_of(n):
    """
    Lazily returns all powers of n, starting with 1
    """
    return LazySequence(__ipowers_of(n))

def __ifibonacci(a = 1, b = 1):
    """
    Lazily returns the fibonacci sequence
    """
    while True:
        yield a
        c = a + b
        a = b
        b = c

def fibonacci(a = 1,b = 1):
    """
    Lazily returns the fibonacci sequence
    """
    return LazySequence(__ifibonacci(a, b))