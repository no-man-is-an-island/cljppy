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
from cljppy.sequence import partition, concat, partition_all
from cljppy.core import identity, plus, doseq
import cljppy.sequence

from processing import Pool

from cljppy.core.Future import Future
from cljppy.reducers.Reducible import Reducible


# def pool(f, partitions, n=4):
#     acc = []
#     for p in partition_all(n, partitions):
#
#         fs = []
#         for r in p:
#             fs.append(Future(f, r))
#
#         for fut in fs:
#             acc.append(fut.deref())
#             fut.finalise()
#
#     return acc



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

