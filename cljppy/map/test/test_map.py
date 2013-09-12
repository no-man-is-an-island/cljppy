from cljppy.core import partial, even, plus, identity
from cljppy.map import *


def test_assoc():
    assert assoc({}) == {}
    assert assoc({"a": 2}, "a", 1) == {"a": 1}
    y = {"a": 2}
    assert assoc(y, "a", 1, "b", 3) == {"a": 1, "b": 3}
    assert y == {"a": 2}


def test_dissoc():
    assert dissoc({}) == {}
    assert dissoc({}, "a") == {}

    x = {"a": 2, "b": 3, "c": 1}
    assert dissoc(x, "a", "b") == {"c": 1}
    assert x == {"a": 2, "b": 3, "c": 1}


def test_merge():
    assert merge() == {}
    assert merge({"a": 1}) == {"a": 1}
    assert merge({"a": 1}, {"a": 2, "b": 2}) == {"a": 2, "b": 2}


def test_merge_with():
    assert merge_with(plus) == {}
    assert merge_with(plus, {"s": 1}) == {"s": 1}
    assert merge_with(plus, {"a": 1}, {"a": 2, "b": 2}) == {"a": 3, "b": 2}


def test_map_vals():
    assert map_vals({}, partial(plus, 1)) == {}
    assert map_vals({"a": 1}, partial(plus, 1)) == {"a": 2}


def test_filter_keys_by_val():
    assert filter_keys_by_val(even, {}) == []
    assert filter_keys_by_val(even, {"a": 1, "b": 2}) == ["b"]


def test_remove_keys_by_val():
    assert remove_keys_bv_val(even, {}) == []
    assert remove_keys_bv_val(even, {"a": 1, "b": 2}) == ["a"]


def test_filter_vals():
    assert filter_vals(even, {}) == {}
    assert filter_vals(even, {"a": 2, 2: 3}) == {"a": 2}


def test_remove_vals():
    assert remove_vals(even, {}) == {}
    assert remove_vals(even, {"a": 2, 2: 3}) == {2: 3}


def test_filter_keys():
    assert filter_keys(even, {}) == {}
    assert filter_keys(even, {1: 2, 2: 3}) == {2: 3}


def test_remove_keys():
    assert remove_keys(even, {}) == {}
    assert remove_keys(even, {1: 2, 2: 3}) == {1: 2}


def test_select_keys():
    assert select_keys({}, []) == {}
    assert select_keys({}, ["a"]) == {}
    assert select_keys({"a": 1, "b": 2}, ["a"]) == {"a": 1}


def test_update_each():
    assert update_each(dict(a=1, b=2, c=3), ("b", "c"), plus, 1) == dict(a=1, b=3, c=4)
    assert update_each(dict(a=1, b=2, c=3), (), plus, 1) == dict(a=1, b=2, c=3)

    # Returns a copy
    original = dict(a=1, b=2, c=3)
    update_each(original, ("a", "b", "c"), plus, 1)
    assert original == dict(a=1, b=2, c=3)

    # Passes none to mapping function if key is not found
    assert update_each(dict(a=1, b=2, c=3), ("a", "z"), identity) == dict(a=1, b=2, c=3, z=None)
