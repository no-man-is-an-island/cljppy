from cljppy.sequence.predicates import *
from cljppy.sequence.generators import natural_numbers
from cljppy.core import even


def test_empty():
    assert empty([])
    assert not empty([1, 2, 3])

    # empty is lazy!
    assert empty(natural_numbers()) == False


def test_not_empty():
    assert not_empty([]) is None
    assert not_empty([1, 2, 3]) ==  [1, 2, 3]


def test_every():
    assert every(even, [])
    assert not every(even, [1, 2, 3])
    assert every(even, [2, 4, 6])


def test_not_every():
    assert not not_every(even, [])
    assert not not_every(even, [2, 4, 6])
    assert not_every(even, [1, 2, 4])


def test_not_any():
    assert not_any(even, [])
    assert not not_any(even, [2, 4, 6])
    assert not_any(even, [1, 3, 5])