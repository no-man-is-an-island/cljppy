#-------------------------------------------------------------------------------
# Name:        cljpy
#
# Purpose:     A library extending python with Clojure-style sequence
#              manipulation.
#
# Example:     take(10, interleave(powers_of(2), powers_of(3), powers_of(5)))
#              => [1, 1, 1, 2, 3, 5, 4, 9, 25, 8, 27]
#
# Author:      David Williams
#
# Created:     27/07/2013
# Copyright:   (c) David Williams 2013
# Licence:     MINE
#-------------------------------------------------------------------------------
import itertools

from cljppy.sequence.lazysequence import LazySequence
from cljppy.map import *
from cljppy.core import *
from cljppy.sequence import *
