from cljppy import natural_numbers, take
from cljppy.sequence.LazySequence import LazySequence


def test_hash_codes_of_lazysequences_make_sense():
    assert hash(LazySequence([0, 1, 2])) == hash(LazySequence(take(3, natural_numbers())))
    assert hash(LazySequence([0, 1, 2, 3])) != hash(LazySequence(take(3, natural_numbers())))


def test_lazy_sequences_are_lazy():
    n = natural_numbers()
    assert take(5, n) == [0, 1, 2, 3, 4]
    assert not n.realised