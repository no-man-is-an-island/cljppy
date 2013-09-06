from cljppy import concat, take_last, mult, apply, partial, plus
from cljppy.fn import *


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
    assert comp() == identity
