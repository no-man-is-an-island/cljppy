#-------------------------------------------------------------------------------
# Name:        cljppy.reducers
#
# Purpose:     This is going to be AWESOME. Prepare yourself.
#
# Author:      David Williams
#
# Created:     27/07/2013
# Copyright:   (c) David Williams 2013
#-------------------------------------------------------------------------------

from processing import *


def thread_off(f):
    """
    Takes something to do, does it on a separate process, and returns
    a  fn that can be called to get the result
    """
    def f_star(q):
        x = f()
        q.put(x)
    q = Queue()
    p = Process(target=f_star, args=[q])
    p.start()
    return q.get

