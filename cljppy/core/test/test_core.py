from cljppy.sequence import concat, take_last
from cljppy.sequence.generators import repeatedly
from cljppy.core import *


def test_identity():
    assert identity(10) == 10
    assert identity("FOOBAR") == "FOOBAR"


def test_constantly():
    fn = constantly(10)
    assert fn() == 10
    assert fn(1, 2, 3) == 10


def test_plus():
    assert plus() == 0
    assert plus(1, 2, 3) == 6


def test_mult():
    assert mult() == 1
    assert mult(1, 2, 3) == 6


def _side_effecter(state):
    """
    Helper fn: Takes a list, appends to it, and returns to it.
    This is useful for testing side effects (need a mutable type for
    this to actually work)
    """
    state.append(0)
    return state


def test_dorun():
    s = []
    assert dorun(repeatedly(partial(_side_effecter, s), 5)) is None
    assert s == [0, 0, 0, 0, 0]


def test_doall():
    s = []
    fn_calls = repeatedly(partial(_side_effecter, s), 5)
    assert doall(fn_calls) == list(fn_calls)
    assert s == [0, 0, 0, 0, 0]


def test_doseq():
    s = [[1], [2], [3]]
    assert doseq(_side_effecter, s) is None
    assert s == [[1, 0], [2, 0], [3, 0]]


def test_apply():
    assert apply(plus) == 0
    assert apply(plus, [1, 2, 3]) == 6
    assert apply(concat, [[1, 2, 3], [4, 5, 6]]) == [1, 2, 3, 4, 5, 6]


def test_partial():
    assert partial(plus)(1, 2, 3) == 6
    assert partial(plus, 1)(2, 3) == 6
    assert partial(take_last, 2)([1, 2, 3, 4]) == [3, 4]
    assert apply(partial, [plus, 1, 2, 3])() == 6


def test_comp():
    assert comp(partial(mult, 3), plus)(1, 2) == 9
