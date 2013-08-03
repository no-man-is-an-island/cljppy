# CljIterTools

A python library extending python's core itertools library with Clojure-like sequence manipulation functions.

STILL UNDER DEVELOPMENT (i.e. use at your own risk)

## Example usage

```
take(5, ifilter(lamda x: (x % 2) == 0, natural_numbers()))

=> [0, 2, 4, 6, 8]
```