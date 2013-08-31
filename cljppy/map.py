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

from cljppy.core import*


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