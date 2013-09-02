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
from cljppy.core import identity

from cljppy.core.Future import Future
from cljppy.reducers.Reducible import Reducible


def map(map_fn, coll):
    def _mapper(reduce_fn):
        def _new_reduce_fn(acc, v):
            return reduce_fn(acc, map_fn(v))

        return _new_reduce_fn
    return Reducible(coll, _mapper)

def reduce(function, iterable, initializer = None):

    reducible = Reducible(iterable, identity)

