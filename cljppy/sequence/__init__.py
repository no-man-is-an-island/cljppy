#-------------------------------------------------------------------------------
# Name:        cljppy.sequence
#
# Purpose:     'Sequence' manipulation functions
#
# Author:      David Williams
#
# Created:     27/07/2013
# Copyright:   (c) David Williams 2013
#-------------------------------------------------------------------------------

import random
import itertools
from sets import Set
from collections import deque

from cljppy.sequence.LazySequence import LazySequence
from cljppy.sequence.predicates import *
from cljppy.sequence.generators import *

def map(f, *iterables):
    """
    Lazy map over one or more iterables (in tandem)..
    OVERRIDES THE STANDARD PYTHON map
    """
    return LazySequence(itertools.imap(f, *iterables))


def __iconj(iterable, x):
    """
    Returns an iterable containing all the elements of the iterable followed by
    x.
    """
    for y in iterable:
        yield y
    yield x

def conj(iterable, x):
    """
    Returns a list containing all tbe elements of the iterable, followed by x
    """
    return LazySequence(__iconj(iterable, x))

def __icons(x, iterable):
    """
    Returns a new iterable with x as the first element, followed by the elements
    of iterable
    """
    yield x
    for y in iter(iterable):
        yield y

def cons(x, iterable):
    """
    Returns a list with x as the first element, followed by the elements of the
    iterable.
    """
    return LazySequence(__icons(x, iterable))

def concat(*args):
    """
    Returns a lazy seq representing the concatenation of the elements in the supplied
    collections.
    """
    return LazySequence(itertools.chain(*args))

def __itake(n, iterable):
    """
    Return an iterable of the first n iterms of the given iterable
    """
    return itertools.islice(iter(iterable), n)

def take(n, iterable):
    """
    Return a list of the first n iterms of the given iterable
    """
    return LazySequence(__itake(n, iterable))

def take_last(n, iterable):
    """
    Returns a list of the last n items of the given iterable.
    Currently will hold the whole iterable in memory..
    """
    # Hmm
    lst = list(iterable)
    l = len(lst)
    return list(itertools.islice(lst, max(0, l - n), l))

def nth(iterable, n, default=None):
    """
    Returns the nth item from an iterable, or a default value
    """
    if type(iterable) in (LazySequence, list, tuple):
        try:
            return iterable[n]
        except IndexError:
            return default
    else:
        return next(itertools.islice(iter(iterable), n, None), default)

def __itake_nth(n, iterable):
    """
    Returns a lazy sequence of every nth item in the iterable
    """
    it = iter(iterable)
    idx = 0
    for x in it:
        if idx % n == 0:
            yield x
        idx += 1

def take_nth(n, iterable):
    """
    Returns a list of every nth item in the iterable
    """
    return LazySequence(__itake_nth(n, iterable))

def rand_nth(iterable):
    """
    Returns a random element from an iterable
    """
    if type(iterable) in (LazySequence, list, tuple):
        l = iterable
    else:
        l = list(iterable)
    r = random.randint(0, len(l) - 1)
    return nth(iterable, r)

def __distinct(iterable):
    """
    Returns an iterator of the distinct items from an iterable.
    """
    s = Set()
    for x in iterable:
        if x not in s:
            yield x
            s.add(x)

def distinct(iterable):
    """
    Returns a lazy seq of the distinct items from an iterable.
    """
    return LazySequence(__distinct(iterable))

def first(iterable, default=None):
    """
    Returns the first value from an iterable, or a default value
    """
    return nth(iterable, 0, default)

def second(iterable, default = None):
    """
    Returns the second item from an iterable, or a default value.
    """
    return first(rest(iterable), default)

def ffirst(iterable, default = None):
    """
    Same as first(first(iterable), default).
    If given an empty iterable, will return default.
    """
    return first(first(iterable, []), default)

def last(iterable, default = None):
    """
    Returns the last element of an iterable.
    Constant time for sequence like things,
    linear time for iterables.
    """
    if type(iterable) in (list, tuple, LazySequence):
        l = len(iterable)

        if l == 0:
            return default
        return iterable[l - 1]
    else:
        it = iter(iterable)
        try:
            x = it.next()
        except StopIteration:
            return default

        for y in it:
            x = y

        return x

def __irest(iterable):
    """
    Takes an iterable, and returns a generator starting at the
    second element.
    """
    firstElement = True
    for x in iterable:
        if firstElement:
            firstElement = False
        else:
            yield x

def rest(iterable):
    """
    Takes an iterable, and returns a list starting at the
    second element.
    """
    return LazySequence(__irest(iterable))

def __inxt(iterable):
    """
    Takes an iterable and returns an iterable starting at the second element.
    Returns None if the iterable is empty
    """
    it1, it2, it3 = itertools.tee(iter(iterable), 3)
    if empty(it1):
        return None
    else:
        if empty(rest(it3)):
            return None
        else:
            return rest(it2)

def nxt(iterable):
    """
    Takes an iterable and returns a list starting at the second element.
    Returns None if the iterable is empty
    """
    n = __inxt(iterable)
    if n == None:
        return None
    else:
        return LazySequence(n)

def fnxt(iterable, default = None):
    """
    Same as first(inext(iterable))
    """
    n = nxt(iterable)
    if n == None:
        return default
    else:
        return first(n, default)

def nnxt(iterable):
    """
    Same as nxt(inxt(iterable))
    """
    n = nxt(iterable)
    if n == None:
        return None
    else:
        return nxt(n)

def __idrop(n, iterable):
    """
    Drops the first n items of the iterable, then returns a new iterable
    """
    m = 0
    for x in iter(iterable):
        if m >= n:
            yield x
        else:
            m += 1

def drop(n, iterable):
    """
    Returns a list without the first n items of the iterable.
    """
    return LazySequence(__idrop(n, iterable))

def __idrop_while(pred, iterable):
    """
    Drops items from an iterable while pred is True. Returns a new iterable
    starting from the first item for while pred(item) is false.
    """
    head = True
    for x in iter(iterable):
        if head and not pred(x):
            head = False
        if not head:
            yield x

def drop_while(pred, iterable):
    """
    Drops items from an iterable while pred is True. Returns a list
    starting from the first item for while pred(item) is false.
    """
    return LazySequence(__idrop_while(pred, iterable))

def drop_last(n, iterable):
    """
    Returns a list of the iterable elements without the last n elements
    """
    # YUCK
    lst = list(iterable)
    l = len(lst)
    return LazySequence(itertools.islice(lst, 0, max(0, l - n)))

def but_last(iterable):
    """
    Returns a list of all elements of an iterable but the last
    """
    return drop_last(1, iterable)

def filter(pred, iterable):
    """
    Returns a list from an iterable with all values for which the predicate
    returns true removed.
    """
    return LazySequence(itertools.ifilter(pred, iterable))

def remove(pred, iterable):
    """
    Returns a list from an iterable with all values for which the predicate
    returns true removed.
    """
    return LazySequence(itertools.ifilterfalse(pred, iterable))

def __imapcat(f, *iterables):
    """
    Takes a function f and zero or more iterables. Returns a generator which
    contains a mapping of f over the concatenation of the iterables.
    """
    return itertools.imap(f, concat(*iterables))

def mapcat(f, *iterables):
    """
    Takes a function f and zero or more iterables. Returns a list which
    contains a mapping of f over the concatenation of the iterables.
    """
    return LazySequence(__imapcat(f, *iterables))

def __imap_indexed(f, iterable):
    """
    Returns a lazy sequence consisting of the result of applying f to 0
    and the first item of coll, followed by applying f to 1 and the second
    item in coll, etc, until coll is exhausted. Thus function f should
    accept 2 arguments, index and item.
    """
    return itertools.imap(f, iterable, natural_numbers())

def map_indexed(f, iterable):
    """
    Returns a list consisting of the result of applying f to 0
    and the first item of coll, followed by applying f to 1 and the second
    item in coll, etc, until coll is exhausted. Thus function f should
    accept 2 arguments, index and item.
    """
    return LazySequence(__imap_indexed(f, iterable))

def __iflatten(listOfLists):
    """
    Flatten one level of nesting, and return an iterable.
    """
    return apply(concat, listOfLists)

def flatten(listOfLists):
    """
    Flatten one level of nesting, returning a list.
    """
    return LazySequence(__iflatten(listOfLists))

def some(pred, iterable):
    """
    Returns the first value x of an iterator where pred(x) is truthy, or None
    otherwise (is returning None idiomatic??)
    """
    for x in iter(iterable):
        if pred(x):
            return x
    return None

def __ikeep(f, iterable):
    """
    Returns a iterable of f(x) for the x in iterable where f(x) is not None.
    NB: If the return value is False, it will still be included
    """
    for x in iter(iterable):
        result = f(x)
        if result != None:
            yield result

def keep(f, iterable):
    """
    Returns a list of f(x) for the x in iterable where f(x) is not None.
    NB: If the return value is False, it will still be included
    """
    return LazySequence(__ikeep(f, iterable))

def __iinterleave(*cs):
    """
    Returns a lazy seq of the first item in each it, then the second etc.
    Continues until the end of the smallest sequence.
    """
    if len(cs) == 0:
        return
    iterators = list(map(iter, cs))

    while True:
        vals = []
        try:
            for it in iterators:
                vals.append(it.next())
        except StopIteration:
            break

        for val in vals:
            yield val


def interleave(*cs):
    """
    Returns a list containing the first item in each it, then the second etc.
    Continues until the end of the smallest sequence
    """
    return LazySequence(__iinterleave(*cs))

def __iinterpose(sep, iterable):
    """
    Returns a lazy seq of the elements of the iterable separated by sep
    """
    return rest(interleave(itertools.repeat(sep), iterable))

def interpose(sep, iterable):
    """
    Returns a list of the elements of the iterable separated by sep
    """
    return LazySequence(__iinterpose(sep, iterable))

def zipmap(keys, vals):
    """
    Returns a dictionary with keys mapped to the corresponding vals
    """
    return dict(zip(keys, vals))

def __ipartition(n, iterable, step = None):
    """
    Returns a lazy sequence of lists of n items each, at offsets step
    apart. If step is not supplied, defaults to n, i.e. the partitions
    do not overlap.
    """
    if step is None:
        step = n
    step_count = step
    last_n = deque(maxlen=n)

    for x in iter(iterable):
        step_count = min(step, step_count + 1)
        last_n.append(x)
        #last_n = take_last(n, last_n)

        if step_count == step and len(last_n) == n:
            y = list(last_n) # Damn mutable data!
            step_count = 0
            yield y

def partition(n, iterable, step = None):
    """
    Returns a list of lists of n items each, at offsets step
    apart. If step is not supplied, defaults to n, i.e. the partitions
    do not overlap.
    """
    return LazySequence(__ipartition(n, iterable, step))

def __ipartition_all(n, iterable, step = None):
    """
    Returns a lazy sequence of lists of n items each, at offsets step
    apart. If step is not supplied, defaults to n, i.e. the partitions
    do not overlap.
    """

    # Can probably do this more prettily. Code golf fail
    if step == None:
        step = n
    step_count = step
    last_n = deque(maxlen=n)

    for x in iter(iterable):
        step_count = min(step, step_count + 1)
        last_n.append(x)

        if step_count == step and len(last_n) == n:
            y = list(last_n) # Damn mutable data!
            step_count = 0
            yield y

    for x in itertools.takewhile(not_empty, iterate(rest, last_n)):
        if step_count == step:
            yield list(x)
            step_count = 0
        step_count += 1

def partition_all(n, iterable, step = None):
    """
    Returns a lazy sequence of lists of n items each, at offsets step
    apart. If step is not supplied, defaults to n, i.e. the partitions
    do not overlap.
    """
    return LazySequence(__ipartition_all(n, iterable, step))

def __ipartition_by(f, iterable):
    """
    Applies f to each value in iterable, splitting it each time f returns
    a new value.  Returns a lazy seq of partitions.
    """
    it1, it2 = itertools.tee(iter(iterable))
    if empty(it1):
        return

    x = it2.next()
    current_value = f(x)
    partition = [x]

    for x in it2:
        value = f(x)
        if current_value != value:
            yield partition
            partition = []
            current_value = value
        partition.append(x)

    yield partition

def partition_by(f, iterable):
    """
    Applies f to each value in iterable, splitting it each time f returns
    a new value.  Returns a list of partitions.
    """
    return LazySequence(__ipartition_by(f, iterable))

def __ireductions(function, iterable, initializer = None):
    """
    Returns a lazy seq of the intermediate values of a reduce  of an iterable
    by f, starting with init. If init is not given, the first value in the
    iterable is used.
    """
    it = iter(iterable)

    if initializer is None:
        try:
            initializer = next(it)
        except StopIteration: # Not sure whether this should throw an exception.
            return # reduce throws one in this case
    accum_value = initializer
    yield accum_value

    for x in it:
        accum_value = function(accum_value, x)
        yield accum_value

def reductions(function, iterable, initializer = None):
    """
    Returns a lazy seq of the intermediate values of a reduce  of an iterable
    by f, starting with init. If init is not given, the first value in the
    iterable is used.
    """
    return LazySequence(__ireductions(function, iterable, initializer))


def frequencies(iterable):
    """
    Returns a dict from distinct items in iterable to the number of times
    they appear.
    """
    f = {}
    for x in iterable:
        if x in f:
            f[x] += 1
        else:
            f[x] = 1
    return f


def reverse(iterable):
    r = list(iterable)
    r.reverse()
    return r
