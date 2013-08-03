# CljIterTools

A python library extending python's core itertools library with Clojure-like sequence manipulation functions. Most sequence operations at http://clojure.org/sequences have been implemented.

***USE AT YOUR OWN RISK***

I mainly just built this for fun. Since Python isn't optimised for this kind of code, these functions can be slow. Also, iterators are mutable in Python, so the following kind of nonsense happens:
```
x = natural_numbers()

take(5, x)

=> [0,1,2,3,4]

take(5, x)

=> [6,7,8,9,10]
```
I might try to sort this out, but, even if I do, it might not be fast enough to be useable. 

## Example usage

Functions which return 'lazy' sequences are prefixed with 'i' (e.g. itake is a lazy version of take). The only exception to this is the functions which return an infinite sequence by default (iterate, repeatedly, natural_numbers etc.), which have only one form.

```
take(5, ireductions(plus, natural_numbers()))
[0, 1, 3, 6, 10]

def even(x):
	return (x % 2) == 0

take(5, ifilter(even, natural_numbers()))

=> [0, 2, 4, 6, 8]

take(3, ipartition(2, powers_of(2)))

=> [[1, 2], [4, 8], [16, 32]]

def ngrams(n, s):
	return rest(imap(partial(take_last, n), ireductions(conj, s, [])))

ngrams(3, [1,2,3,4,5])

=>[[1], [1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]]
```

## TODO

- Implement an immutable lazy primitve, so that repeatedly using a 'lazy' sequence doesn't give different results 