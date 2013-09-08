from cljppy import natural_numbers, take
from cljppy.sequence.LazySequence import LazySequence


def test_hash_codes_of_lazysequences_make_sense():
    assert hash(LazySequence([0, 1, 2])) == hash(LazySequence(take(3, natural_numbers())))
    assert hash(LazySequence([0, 1, 2, 3])) != hash(LazySequence(take(3, natural_numbers())))