from cljppy import mult, inc
from cljppy.reducers import rreduce, rmap


def increment_and_multiply_range(x):
    a = 1
    for b in range(x):
        a *= b + 1
    return a


def test_reduce_works():
    assert rreduce(mult, rmap(inc, range(1000))) == increment_and_multiply_range(1000)
    assert rreduce(mult, rmap(inc, range(10000))) == increment_and_multiply_range(10000)