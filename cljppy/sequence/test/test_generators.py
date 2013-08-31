from cljppy.sequence.generators import *
from cljppy.sequence import take
from cljppy.core import inc


def test_cycle():
    assert take(5, cycle([1, 2, 3])) == [1, 2, 3, 1, 2]
    assert take(5, cycle([])) == []
    # assert take(5, cycle(iter([])) == [] # Hmm.. can't see a nice way to do this


def test_repeatedly():
    # NB: plus has a zero arity form that returns 0 (the identity)
    assert list(repeatedly(plus, 0)) == []
    assert list(repeatedly(plus, 5)) == [0, 0, 0, 0, 0]
    assert take(5, repeatedly(plus)) == [0, 0, 0, 0, 0]


def test_iterate():
    assert list(iterate(inc, 0, 5)) == [0, 1, 2, 3, 4]
    assert list(iterate(lambda x: x * 2, 1, 5)) == [1, 2, 4, 8, 16]
    assert take(5, iterate(inc, 1)) == [1, 2, 3, 4, 5]
