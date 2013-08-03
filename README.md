# CljIterTools

A python library extending python's core itertools library with Clojure-like sequence manipulation functions. Most sequence operations at http://clojure.org/sequences have been implemented.

STILL UNDER DEVELOPMENT (i.e. use at your own risk). Since Python isn't optimised for this kind of code, these functions can be slow. Also, iterators are mutable in Python, so the following kind of nonsense happens:
```
x = natural_numbers()

take(5, x)

=> [0,1,2,3,4]

take(5, x)

=> [6,7,8,9,10]
```

## Example usage

Functions which return 'lazy' sequences are prefixed with 'i' (e.g. itake is a lazy version of take). The only exception to this is the functions which return an infinite sequence by default (iterate, repeatedly, natural_numbers etc.), which have only one form.

```
take(5, ifilter(lambda x: (x % 2) == 0, natural_numbers()))

=> [0, 2, 4, 6, 8]

take(3, ipartition(2, powers_of(2)))

=> [[1, 2], [4, 8], [16, 32]]

```

## TODO

- Implement an immutable lazy primitve, so that repeatedly using a 'lazy' sequence doesn't give different results 