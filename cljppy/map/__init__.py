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
from cljppy.core import partial
from cljppy.sequence import partition


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


def map_vals(m, f, *args):
    """
    Returns a copy of m with f applied to each value.
    """
    r = {}

    for k, v in m.iteritems():
        r[k] = f(v, *args)

    return r


def map_keys(m, f, *args):
    """
    Returns a copy of m with f applied to each key
    """
    m2 = {}
    for k in m.iterkeys():
        m2[f(k, *args)] = m[k]

    return m2


def filter_keys_by_val(p, m):
    """
    Returns a seq of keys for which p(val) returns true
    """
    keys = []

    for k, v in m.iteritems():
        if p(v):
            keys.append(k)

    return keys


def remove_keys_bv_val(p, m):
    """
    Returns a seq of keys for which p(val) returns false
    """
    return filter_keys_by_val(lambda v: not p(v), m)


def filter_vals(p, m):
    """
    Returns a new map containing those key value pairs where
    p(value) is true
    """
    r = {}
    for k, v in m.iteritems():
        if p(v):
            r[k] = v

    return r


def remove_vals(p, m):
    """
    Returns a new map containing those key value pairs where
    p(value) is false
    """
    return filter_vals(lambda v: not p(v), m)


def filter_keys(p, m):
    """
    Returns a copy of the map containing the key value pairs where
    p(key) is true
    """
    r = {}
    for k, v in m.iteritems():
        if p(k):
            r[k] = v

    return r


def remove_keys(p, m):
    """
    Returns a copy of the map containing the key value pairs where
    p(key) is false
    """
    return filter_keys(lambda v: not p(v), m)


def select_keys(m, ks):
    r = {}
    for k in ks:
        if k in m:
            r[k] = m[k]
    return r


def update_each(m, ks, f, *args):
    """
    Returns a shallow copy of m, updating the values for each of the
    given keys in a map where f is a function that takes each previous
    value and the supplied args and returns a new value.
    """
    copy = m.copy()
    for k in ks:
        copy[k] = f(copy.get(k), *args)
    return copy


def keyword(name):
    """
    Returns a function that takes a map and return map[name]
    """
    def _fn(m):
        return m.get(name, None)
    return _fn