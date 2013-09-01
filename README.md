# Cljppy

<img src="http://www.psdgraphics.com/file/isolated-paper-clip.jpg" width=200px />

A python library extending python with Clojure-like lazy sequences and sequence manipulation functions. Most sequence operations at http://clojure.org/sequences have been implemented.

API Docs can be found <a href="http://no-man-is-an-island.github.io/cljppy/index.html" target="_blank">here</a>.
I mainly just built this for fun. Since Python isn't optimised for this kind of code, these functions can be slow.

## Example usage

All functions return LazySequence objects, which are immutable, lazily generated from the iterator which generates them, and are considered equal to a list containing the same data.
Every function that takes a LazySequence will take any kind of iterable object, but be aware that most functions will exhaust iterators (iterators=evil)

```
natural_numbers()
=> [0, 1, 2, 3, 4, ...]

take(5, reductions(plus, natural_numbers()))
=> [0, 1, 3, 6, 10]

take(5, filter(even, natural_numbers()))
=> [0, 2, 4, 6, 8]

take(3, partition(2, powers_of(2)))
=> [[1, 2], [4, 8], [16, 32]]

def ngrams(n, s):
	return rest(map(partial(take_last, n), reductions(conj, s, [])))

ngrams(3, [1,2,3,4,5])
=> [[1], [1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]]
```

## Dependencies

python-dev (if you want to use the reducers namespace)
