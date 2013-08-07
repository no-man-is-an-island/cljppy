#-------------------------------------------------------------------------------
# Name:        test_cljitertools
# Purpose:
#
# Author:      David Williams
#
# Created:     28/07/2013
# Copyright:   (c) David Williams 2013
# Licence:     MINE
#-------------------------------------------------------------------------------
from cljitertools import *

def test_identity():
    assert identity(10) == 10
    assert identity("FOOBAR") == "FOOBAR"

def test_constantly():
    fn = constantly(10)
    assert fn() == 10
    assert fn(1,2,3) == 10

def test_plus():
    assert plus() == 0
    assert plus(1,2,3) == 6

def test_mult():
    assert mult() == 1
    assert mult(1,2,3) == 6

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
    assert dorun(repeatedly(partial(_side_effecter, s), 5)) == None
    assert s == [0,0,0,0,0]

def test_doall():
    s = []
    fn_calls = repeatedly(partial(_side_effecter, s), 5)
    assert doall(fn_calls) == list(fn_calls)
    assert s == [0,0,0,0,0]

def test_doseq():
    s = [[1], [2], [3]]
    assert doseq(_side_effecter, s) == None
    assert s == [[1,0], [2,0], [3,0]]

def test_apply():
    assert apply(plus) == 0
    assert apply(plus, [1,2,3]) == 6
    assert apply(concat, [[1,2,3], [4,5,6]]) == [1,2,3,4,5,6]

def test_partial():
    assert partial(plus)(1,2,3) == 6
    assert partial(plus, 1)(2,3) == 6
    assert partial(take_last, 2)([1,2,3,4]) == [3, 4]
    assert apply(partial, [plus,1,2,3])() == 6

def test_empty():
    assert empty([]) == True
    assert empty([1,2,3]) == False
    assert empty(rest([1])) == True

    # empty is lazy!
    assert empty(natural_numbers()) == False

def test_not_empty():
    assert not_empty([]) == None
    assert not_empty([1,2,3]) ==  [1,2,3]

def _even(x):
    """
    Predicate to check if an int is even
    """
    return (x % 2) == 0

def test_every():
    assert every(_even, []) == True
    assert every(_even, [1,2,3]) == False
    assert every(_even, [2,4,6]) == True

def test_not_every():
    assert not_every(_even, []) == False
    assert not_every(_even, [2,4,6]) == False
    assert not_every(_even, [1,2,4]) == True

def test_not_any():
    assert not_any(_even, []) == True
    assert not_any(_even, [2,4,6]) == False
    assert not_any(_even, [1,3,5]) == True

def test_conj():
    assert conj([1,2,3], 4) == [1,2,3,4]

def test_cons():
    assert cons(1, [2,3]) == [1,2,3]
    assert cons(-1, take(4, natural_numbers())) == [-1,0,1,2,3]
    assert take(5, cons(-1, natural_numbers())) == [-1,0,1,2,3]

def test_concat():
    assert concat([1,2,3], [4,5,6]) == [1,2,3,4,5,6]

def test_take():
    assert take(5, natural_numbers()) == [0,1,2,3,4]
    assert take(0, natural_numbers()) == []
    assert take(5, []) == []

    # itake is lazy - it's one of those tests that either works or crashes your
    # machine
    assert take(5, take(1000000000000000000, natural_numbers())) == [0,1,2,3,4]

def test_take_last():
    assert take_last(2, iter([1,2,3,4,5])) == [4,5]
    assert take_last(1, []) == []
    assert take_last(5, [1,2,3]) == [1,2,3]
    assert take_last(0, [1]) == []

def test_nth():
    assert nth(iter([1,2,3]), 1) == 2
    assert nth([1,2,3], 1) == 2
    assert nth([], 1, None) == None
    assert nth([1,2], 4, None) == None

def test_take_nth():
    assert take_nth(2, []) == []
    assert take_nth(2, [1,2,3,4,5]) == [1,3,5]
    assert take(3, take_nth(3, fibonacci())) == [1,3,13]

def test_first():
    assert first([], None) == None
    assert first([1,2,3]) == 1
    assert first(natural_numbers()) == 0

def test_ffirst():
    assert ffirst([[]], None) == None
    assert ffirst([], None) == None
    assert ffirst([[1], [2]]) == 1

def test_last():
    assert last([], None) == None
    assert last(iter([1,2,3])) == 3
    assert last([1,2,3]) == 3

def test_second():
    assert second([1,2,3]) == 2
    assert second([], None) == None
    assert second([1], None) == None

def test_rest():
    assert rest([]) == []
    assert rest([1,2,3]) == [2,3]
    assert first(rest(natural_numbers())) == 1

def test_nxt():
    assert nxt([]) == None
    assert nxt([1]) == None
    assert nxt([1,2,3]) == [2,3]
    assert first(nxt(natural_numbers())) == 1

def test_fnxt():
    assert fnxt([], None) == None
    assert fnxt([1], None) == None
    assert fnxt([1,2]) == 2

def test_nnxt():
    assert nnxt([]) == None
    assert nnxt([1]) == None
    assert nnxt([2,3]) == None
    assert nnxt([1,2,3]) == [3]

def test_drop():
    assert drop(5, []) == []
    assert drop(1, [1,2,3]) == [2,3]
    assert take(5, drop(5, natural_numbers())) == [5,6,7,8,9]

def test_drop_while():
    assert drop_while(_even, []) == []
    assert drop_while(_even, [2,4,6]) == []
    assert drop_while(_even, [2,4,1,3,4,5]) == [1,3,4,5]
    assert first(drop_while(lambda x: x < 100, powers_of(2))) == 128

def test_drop_last():
    assert drop_last(1, iter([1,2,3])) == [1,2]
    assert drop_last(1, []) == []
    assert drop_last(3, [1,2]) == []
    assert drop_last(2, [1,2,3,4,5]) == [1,2,3]

def test_but_last():
    assert but_last([]) == []
    assert but_last([1,2,3]) == [1,2]
    assert but_last([2]) == []

def test_remove():
    assert remove(_even, [1,2,3,4]) == [1,3]
    assert remove(_even, []) == []

_inc = partial(plus, 1)

def test_mapcat():
    assert mapcat(_inc, []) == []
    assert mapcat(_inc, [1,2,3]) == [2,3,4]
    assert mapcat(_inc, [1,2,3], [4,5,6]) == [2,3,4,5,6,7]
    assert take(5, mapcat(_inc, [1,2], natural_numbers())) == [2,3,1,2,3]

def test_map_indexed():
    assert map_indexed(plus, []) == []
    assert map_indexed(plus, [1,2,3]) == [1,3,5]

def test_flatten():
    assert flatten([]) == []
    assert flatten([[]]) == []
    assert flatten([[1,2,3], [4,5,6]]) == [1,2,3,4,5,6]
    assert take(5, flatten([[1,2,3], natural_numbers()])) == [1,2,3,0,1]

def test_some():
    assert some(_even, [1,2,3]) == 2
    assert some(_even, [1,3]) == None
    assert some(_even, []) == None

def _keep_fn(x):
    if (x % 2) == 0:
        return x + 1
    else:
        return None

def test_keep():
    assert keep(_keep_fn, []) == []
    assert keep(_keep_fn, [1,2,3]) == [3]
    assert take(5, keep(_keep_fn, natural_numbers())) == [1,3,5,7,9]

def test_interleave():
    assert interleave([1,2,3,4,5]) == [1,2,3,4,5]
    assert interleave() == []
    assert interleave([1,3], [2,4]) == [1,2,3,4]
    assert interleave(repeat(1), [2,4]) == [1,2,1,4]
    assert take(5, interleave(powers_of(2), powers_of(3))) == [1,1,2,3,4]
    assert take(5, apply(interleave, map(powers_of, [2,3]))) == [1,1,2,3,4]

def test_interpose():
    assert interpose(1, []) == []
    assert interpose(1, [2,2,2]) == [2,1,2,1,2]
    assert take(5, interpose(1, natural_numbers())) == [0,1,1,1,2]

def test_zipmap():
    assert zipmap([], []) == {}
    assert zipmap(["a", "b"], [1,2]) == {"a" : 1, "b" : 2}

def test_partition():
    assert partition(2, []) == []
    assert partition(2, [1,2,3,4]) == [[1,2], [3,4]]
    assert partition(2, [1,2,3,4,5]) == [[1,2], [3,4]]
    assert partition(2, [1,2,3,4,5], 1) == [[1,2], [2,3], [3,4], [4,5]]
    assert partition(2, [1,2,3,4,5], 3) == [[1,2], [4,5]]
    assert partition(10, [1,2,3]) == []
    assert take(3, partition(2, natural_numbers(), 1)) == [[0,1], [1,2], [2,3]]

def test_partition_all():
    assert partition_all(2, []) == []
    assert partition_all(2, [1,2,3,4]) == [[1,2], [3,4]]
    assert partition_all(2, [1,2,3,4,5]) == [[1,2], [3,4], [5]]
    assert partition_all(2, [1,2,3,4,5], 1) == [[1,2], [2,3], [3,4], [4,5], [5]]
    assert partition_all(2, [1,2,3,4,5], 3) == [[1,2], [4,5]]
    assert partition_all(10, [1,2,3]) == [[1,2,3]]
    assert take(2, partition_all(2, natural_numbers(), 1)) == [[0,1], [1,2]]

def test_partition_by():
    assert partition_by(_inc, []) == []
    assert partition_by(_inc, [0,0]) == [[0,0]]
    assert partition_by(_inc, [0,0,1,1]) == [[0,0], [1,1]]
    assert take(2, partition_by(identity, natural_numbers())) == [[0], [1]]

def test_reductions():
    assert reductions(concat, []) == []
    assert reductions(concat, [[1], [2]], []) == [[], [1], [1,2]]
    assert take(3, reductions(conj, natural_numbers(), [])) == [[], [0], [0,1]]

def test_repeatedly():
    # NB: plus has a zero arity form that returns 0 (the identity)
    assert list(repeatedly(plus, 0)) == []
    assert list(repeatedly(plus, 5)) == [0,0,0,0,0]
    assert take(5, repeatedly(plus)) == [0,0,0,0,0]

def test_iterate():
    assert list(iterate(_inc, 0, 5)) == [0,1,2,3,4]
    assert list(iterate(lambda x: x * 2, 1, 5)) == [1,2,4,8,16]
    assert take(5, iterate(_inc, 1)) == [1,2,3,4,5]