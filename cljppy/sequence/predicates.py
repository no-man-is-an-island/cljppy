#-------------------------------------------------------------------------------
# Name:        cljppy.sequence.preddicates
#
# Purpose:     Predicates that act on sequences
#
# Author:      David Williams
#
# Created:     27/07/2013
# Copyright:   (c) David Williams 2013
#-------------------------------------------------------------------------------

def empty(iterable):
    """
    Predicate: is the iterable empty.
    Warning - this will exhaust an iterator if passed in.
    """
    it = iter(iterable)
    try:
        it.next()
    except StopIteration:
        return True
    return False


def not_empty(iterable):
    """
    Returns None if the iterable is empty, or the iterable if it isn't.
    Warning - this will exhaust an iterator if passed in.
    """
    if not(empty(iterable)):
        return iterable


def every(pred, iterable):
    """
    Predicate: pred(x) is true for every x in the iterable
    Warning - this will exhaust an iterator if passed in.
    """
    for x in iter(iterable):
        if not pred(x):
            return False
    return True


def not_every(pred, iterable):
    """
    Predicate: pred(x) is false for some x in the iterable
    Warning - this will exhaust an iterator if passed in.
    """
    for x in iter(iterable):
        if not pred(x):
            return True
    return False


def not_any(pred, iterable):
    """
    Predicate: pred(x) is false for every x in the iterable
    Warning - this will exhaust an iterator if passed in.
    """
    return every(lambda x: not pred(x), iterable)