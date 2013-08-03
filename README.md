# CljIterTools

A python library extending python's core itertools library with Clojure-like sequence manipulation functions. Most sequence operations at http://clojure.org/sequences have been implemented.

STILL UNDER DEVELOPMENT (i.e. use at your own risk)

## Example usage

```
take(5, ifilter(lambda x: (x % 2) == 0, natural_numbers()))

=> [0, 2, 4, 6, 8]

take(3, ipartition(2, powers_of(2)))

=> [[1, 2], [4, 8], [16, 32]]


```

## TODO

- Implement an immutable lazy primitve, so that repeatedly using a 'lazy' sequence doesn't give different results 