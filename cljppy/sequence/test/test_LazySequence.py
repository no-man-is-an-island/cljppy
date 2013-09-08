from cljppy.sequence.LazySequence import LazySequence


def test_hash_codes_of_lazysequences_make_sense():
    assert hash(LazySequence([1,2,3])) == hash(LazySequence([1,2,3]))