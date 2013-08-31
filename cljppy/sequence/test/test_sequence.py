from cljppy.sequence import *


def test_frequencies():
    assert frequencies([]) == {}
    assert frequencies([1, 2, 3]) == {1: 1, 2: 1, 3: 1}
    assert frequencies([1, 2, 3, 1, 2, 3]) == {1: 2, 2: 2, 3: 2}


def test_conj():
    assert conj([1, 2, 3], 4) == [1, 2, 3, 4]


def test_cons():
    assert cons(1, [2, 3]) == [1, 2, 3]
    assert cons(-1, take(4, natural_numbers())) == [-1, 0, 1, 2, 3]
    assert take(5, cons(-1, natural_numbers())) == [-1, 0, 1, 2, 3]


def test_concat():
    assert concat([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6]


def test_take():
    assert take(5, natural_numbers()) == [0, 1, 2, 3, 4]
    assert take(0, natural_numbers()) == []
    assert take(5, []) == []

    # itake is lazy - it's one of those tests that either works or crashes your
    # machine
    assert take(5, take(1000000000000000000, natural_numbers())) == [0, 1, 2, 3, 4]


def test_take_last():
    assert take_last(2, iter([1, 2, 3, 4, 5])) == [4, 5]
    assert take_last(1, []) == []
    assert take_last(5, [1, 2, 3]) == [1, 2, 3]
    assert take_last(0, [1]) == []


def test_nth():
    assert nth(iter([1, 2, 3]), 1) == 2
    assert nth([1, 2, 3], 1) == 2
    assert nth([], 1, None) is None
    assert nth([1, 2], 4, None) is None


def test_take_nth():
    assert take_nth(2, []) == []
    assert take_nth(2, [1, 2, 3, 4, 5]) == [1, 3, 5]
    assert take(3, take_nth(3, fibonacci())) == [1, 3, 13]


def test_distinct():
    assert distinct([1, 2, 3, 4, 1, 2]) == [1, 2, 3, 4]
    assert take(5, distinct(natural_numbers())) == [0, 1, 2, 3, 4]


def test_first():
    assert first([], None) is None
    assert first([1, 2, 3]) == 1
    assert first(natural_numbers()) == 0


def test_ffirst():
    assert ffirst([[]], None) is None
    assert ffirst([], None) is None
    assert ffirst([[1], [2]]) == 1


def test_last():
    assert last([], None) is None
    assert last(iter([1, 2, 3])) == 3
    assert last([1, 2, 3]) == 3


def test_second():
    assert second([1, 2, 3]) == 2
    assert second([], None) is None
    assert second([1], None) is None


def test_rest():
    assert rest([]) == []
    assert rest([1, 2, 3]) == [2, 3]
    assert first(rest(natural_numbers())) == 1


def test_nxt():
    assert nxt([]) is None
    assert nxt([1]) is None
    assert nxt([1, 2, 3]) == [2, 3]
    assert first(nxt(natural_numbers())) == 1


def test_fnxt():
    assert fnxt([], None) is None
    assert fnxt([1], None) is None
    assert fnxt([1, 2]) == 2


def test_nnxt():
    assert nnxt([]) is None
    assert nnxt([1]) is None
    assert nnxt([2, 3]) is None
    assert nnxt([1, 2, 3]) == [3]


def test_drop():
    assert drop(5, []) == []
    assert drop(1, [1, 2, 3]) == [2, 3]
    assert take(5, drop(5, natural_numbers())) == [5, 6, 7, 8, 9]


def test_drop_while():
    assert drop_while(even, []) == []
    assert drop_while(even, [2, 4, 6]) == []
    assert drop_while(even, [2, 4, 1, 3, 4, 5]) == [1, 3, 4, 5]
    assert first(drop_while(lambda x: x < 100, powers_of(2))) == 128


def test_drop_last():
    assert drop_last(1, iter([1, 2, 3])) == [1, 2]
    assert drop_last(1, []) == []
    assert drop_last(3, [1, 2]) == []
    assert drop_last(2, [1, 2, 3, 4, 5]) == [1, 2, 3]


def test_but_last():
    assert but_last([]) == []
    assert but_last([1, 2, 3]) == [1, 2]
    assert but_last([2]) == []


def test_remove():
    assert remove(even, [1, 2, 3, 4]) == [1, 3]
    assert remove(even, []) == []


def test_mapcat():
    assert mapcat(inc, []) == []
    assert mapcat(inc, [1, 2, 3]) == [2, 3, 4]
    assert mapcat(inc, [1, 2, 3], [4, 5, 6]) == [2, 3, 4, 5, 6, 7]
    assert take(5, mapcat(inc, [1, 2], natural_numbers())) == [2, 3, 1, 2, 3]


def test_map_indexed():
    assert map_indexed(plus, []) == []
    assert map_indexed(plus, [1, 2, 3]) == [1, 3, 5]


def test_flatten():
    assert flatten([]) == []
    assert flatten([[]]) == []
    assert flatten([[1, 2, 3], [4, 5, 6]]) == [1, 2, 3, 4, 5, 6]
    assert take(5, flatten([[1, 2, 3], natural_numbers()])) == [1, 2, 3, 0, 1]


def test_some():
    assert some(even, [1, 2, 3]) == 2
    assert some(even, [1, 3]) is None
    assert some(even, []) is None


def _keep_fn(x):
    if (x % 2) == 0:
        return x + 1
    else:
        return None


def test_keep():
    assert keep(_keep_fn, []) == []
    assert keep(_keep_fn, [1, 2, 3]) == [3]
    assert take(5, keep(_keep_fn, natural_numbers())) == [1, 3, 5, 7, 9]


def test_interleave():
    assert interleave([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert interleave() == []
    assert interleave([1, 3], [2, 4]) == [1, 2, 3, 4]
    assert interleave(repeat(1), [2, 4]) == [1, 2, 1, 4]
    assert take(5, interleave(powers_of(2), powers_of(3))) == [1, 1, 2, 3, 4]
    assert take(5, apply(interleave, map(powers_of, [2, 3]))) == [1, 1, 2, 3, 4]


def test_interpose():
    assert interpose(1, []) == []
    assert interpose(1, [2, 2, 2]) == [2, 1, 2, 1, 2]
    assert take(5, interpose(1, natural_numbers())) == [0, 1, 1, 1, 2]


def test_zipmap():
    assert zipmap([], []) == {}
    assert zipmap(["a", "b"], [1, 2]) == {"a": 1, "b": 2}


def test_partition():
    assert partition(2, []) == []
    assert partition(2, [1, 2, 3, 4]) == [[1, 2], [3, 4]]
    assert partition(2, [1, 2, 3, 4, 5]) == [[1, 2], [3, 4]]
    assert partition(2, [1, 2, 3, 4, 5], 1) == [[1, 2], [2, 3], [3, 4], [4, 5]]
    assert partition(2, [1, 2, 3, 4, 5], 3) == [[1, 2], [4, 5]]
    assert partition(10, [1, 2, 3]) == []
    assert take(3, partition(2, natural_numbers(), 1)) == [[0, 1], [1, 2], [2, 3]]


def test_partition_all():
    assert partition_all(2, []) == []
    assert partition_all(2, [1, 2, 3, 4]) == [[1, 2], [3, 4]]
    assert partition_all(2, [1, 2, 3, 4, 5]) == [[1, 2], [3, 4], [5]]
    assert partition_all(2, [1, 2, 3, 4, 5], 1) == [[1, 2], [2, 3], [3, 4], [4, 5], [5]]
    assert partition_all(2, [1, 2, 3, 4, 5], 3) == [[1, 2], [4, 5]]
    assert partition_all(10, [1, 2, 3]) == [[1, 2, 3]]
    assert take(2, partition_all(2, natural_numbers(), 1)) == [[0, 1], [1, 2]]


def test_partition_by():
    assert partition_by(inc, []) == []
    assert partition_by(inc, [0, 0]) == [[0, 0]]
    assert partition_by(inc, [0, 0, 1, 1]) == [[0, 0], [1, 1]]
    assert take(2, partition_by(identity, natural_numbers())) == [[0], [1]]


def test_reductions():
    assert reductions(concat, []) == []
    assert reductions(concat, [[1], [2]], []) == [[], [1], [1, 2]]
    assert take(3, reductions(conj, natural_numbers(), [])) == [[], [0], [0, 1]]