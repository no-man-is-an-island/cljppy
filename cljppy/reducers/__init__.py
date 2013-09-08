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
from cljppy import partition_all, partial
from cljppy.reducers.FuturePool import FuturePool
from cljppy.reducers.Reducible import Reducible


def p_reduce(reduce_fn, coll, chunksize=2048):
    """
    Parallel reduce. Uses a pool of <cpus> workers, and splits the
    collection into <chunk_size=2048> size chunks
    """
    r_fn = partial(reduce, reduce_fn)
    return r_fn(FuturePool(r_fn, partition_all(chunksize, coll), chunksize=1).deref())


def p_map(map_fn, coll):
    """
    Parallel map. Map fn needs to be pretty expensive to get over co-ordination
    overhead.
    """
    return FuturePool(map_fn, coll, chunksize=4086).deref()


def map(map_fn, coll):
    def _mapper(reduce_fn):
        def _new_reduce_fn(acc, v):
            return reduce_fn(acc, map_fn(v))

        return _new_reduce_fn
    return Reducible(coll, _mapper)


#def reduce(function, iterable, initializer=None):
#
#   reducible = Reducible(iterable, identity)
#   return reducible.reduce(function, initializer)

