#-------------------------------------------------------------------------------
# Name:        cljppy.reducers
#
# Purpose:     Clojure-style parallel reducers (that actually get you parallelism with multiprocessing!)
#              This is going to be AWESOME. Prepare yourself.
#
# Author:      David Williams
#
# Created:     27/07/2013
# Copyright:   (c) David Williams 2013
#-------------------------------------------------------------------------------
from cljppy import identity, conj
from cljppy.reducers.FuturePool import FuturePool
from cljppy.reducers.Reducible import Reducible, fold


def p_map(map_fn, coll, chunksize=4086):
    """
    Parallel map. Map fn needs to be pretty expensive to get over co-ordination
    overhead.
    """
    return FuturePool(map_fn, coll, chunksize=chunksize).deref()


def rmap(map_fn, coll):
    def _mapper(reduce_fn):
        def _new_reduce_fn(acc, v):
            return reduce_fn(acc, map_fn(v))

        return _new_reduce_fn
    return Reducible(coll, _mapper)


def rfilter(filter_fn, coll):
    def _filterer(reduce_fn):
        def _new_reduce_fn(acc, v):
            if filter_fn(v):
                return reduce_fn(acc, v)
            else:
                return acc
        return _new_reduce_fn
    return Reducible(coll, _filterer)


def rreduce(function, iterable, init=None):
    reducible = Reducible(iterable, identity)
    return reducible.reduce(function, init)


def into(coll1, coll2):
    return rreduce(conj, coll2, coll1)