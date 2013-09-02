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

from processing import *


def dispatch(f):
    """
    Takes something to do, does it on a separate process, and returns
    a fn that can be called to get the result (but will block forever
    the second time it is called, so beware!!)
    """
    def f_star(q):
        q.put(f())
    q = Queue()
    p = Process(target=f_star, args=[q])
    p.start()
    return q.get


