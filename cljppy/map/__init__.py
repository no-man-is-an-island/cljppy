#-------------------------------------------------------------------------------
# Name:        cljppy.map
#
# Purpose:     'Map' manipulation functions
#
# Author:      David Williams
#
# Created:     27/07/2013
# Copyright:   (c) David Williams 2013
#-------------------------------------------------------------------------------
from cljppy.sequence import partition
from cljppy.core import *

def __assoc(m, p):
    """
    Returns a copy of a map m with p[0] mapped to p[1]
    """
    s = m.copy()
    s[p[0]] = p[1]
    return s


def assoc(m, *args):
    """
    Returns a copy of m with the given keys mapped to the given vals:

    assoc({}, "a", 1, "b", 3)
    => {'a': 1, 'b': 3}
    """
    return reduce(__assoc, partition(2, args), m)


def dissoc(m, *keys):
    """
    Returns a copy of m with the mappings for the given keys removed.
    """
    r = m.copy()
    for key in keys:
        if key in r:
            del r[key]

    return r


def pairwise_merge(f, m1, m2):
    """
    Pairwise merge with a merge fn to decide conflicts
    """
    result_dict = m1.copy()  # shallow copy

    for k, v in m2.iteritems():
        if k in m1:
            result_dict[k] = f(m1[k], v)
        else:
            result_dict[k] = v

    return result_dict


def merge(*maps):
    """
    Returns a dict that consists of the rest of the dict conj-ed onto
    the first. If a key occurs in more than one dict, the mapping from
    the latter (left-to-right) will be the mapping in the result.
    """
    return reduce(partial(pairwise_merge, lambda x, y: y), maps, {})


def merge_with(f, *maps):
    """
    Returns a dict that consists of the rest of the maps conj-ed onto
    the first. If a key occurs in more than one dict, the mapping(s)
    from the latter (left-to-right) will be combined with the mapping in
    the result by calling (f val-in-result val-in-latter).
    """
    return reduce(partial(pairwise_merge, f), maps, {})