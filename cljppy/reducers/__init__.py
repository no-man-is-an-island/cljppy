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
from cljppy import partition_all, partial, identity
from cljppy.reducers.FuturePool import FuturePool
from cljppy.reducers.Reducible import Reducible


def p_map(map_fn, coll):
    """
    Parallel map. Map fn needs to be pretty expensive to get over co-ordination
    overhead.
    """
    return FuturePool(map_fn, coll, chunksize=4086).deref()


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
    return Reducible(coll, _filterer)


def rreduce(function, iterable, initializer=None):
    reducible = Reducible(iterable, identity)
    return reducible.reduce(function)

