# CljIterTools

A python library extending python's core itertools library with Clojure-like sequence manipulation functions. Most sequence operations at http://clojure.org/sequences have been implemented.

***USE AT YOUR OWN RISK***

I mainly just built this for fun. Since Python isn't optimised for this kind of code, these functions can be slow.

## Example usage

All functions return LazySequence objects, which behave like lists (and can be equal to a list containing the same data), but are lazily evaluated. Everything should work when passed a list, tuple or iterator though (but iterators are mutable and evil, so please try to avoid using them).

```
take(5, reductions(plus, natural_numbers()))
=> [0, 1, 3, 6, 10]

def even(x):
	return (x % 2) == 0

take(5,ifilter(even, natural_numbers()))
=> [0, 2, 4, 6, 8]

take(3, partition(2, powers_of(2)))
=> [[1, 2], [4, 8], [16, 32]]

def ngrams(n, s):
	return rest(map(partial(take_last, n), reductions(conj, s, [])))

ngrams(3, [1,2,3,4,5])
=> [[1], [1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]]
```
