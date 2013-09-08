#-------------------------------------------------------------------------------
# Name:        cljppy.sequence.lazysequence
#
# Purpose:     Class definition for an immutable lazy sequence
#
# Author:      David Williams
#
# Created:     27/07/2013
# Copyright:   (c) David Williams 2013
#-------------------------------------------------------------------------------

class LazySequenceIterator(object):
    def __init__(self, lazyseq):
        self.__lazyseq = lazyseq
        self.__index = 0

    def next(self):
        try:
            self.__index += 1
            return self.__lazyseq[self.__index - 1]
        except IndexError:
            raise StopIteration

    def reset(self):
        self.__index = 0

    def __iter__(self):
        return self


class LazySequence(object):
    def __init__(self, source, printlength = 100):
        """
        Takes a 'source', which can be a generator or an
        iterable object.
        """
        self.realised = False
        self.__realised_segment = ()
        self.__realised_segment_size = 0
        self.__source_it = iter(source)
        self.print_length = printlength
        try:
            self.__realised_segment = self.__realised_segment + (self.__source_it.next(),)
            self.__realised_segment_size += 1
        except StopIteration:
            self.realised = True

    def __getslice__(self, start, stop):
        s = []
        for idx in range(start, stop):
            s.append(self[idx])
        return s

    def __getitem__(self, item):
        if item >= self.__realised_segment_size:
            if self.realised:
                raise IndexError("index out of range")
            while (not self.realised) and self.__realised_segment_size != item + 1:
                self.realise_next()
            return self[item]

        return self.__realised_segment[item]

    def __len__(self):
        if not self.realised:
            self.realise_all()
        return len(self.__realised_segment)

    def __iter__(self):
        return LazySequenceIterator(self)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        self.realise_to(100)

        if self.realised and self.print_length >= self.__realised_segment_size:
            return str(self.__realised_segment)

        return "[" + ', '.join(map(str, self.__realised_segment)[0:self.print_length]) + ", ...]"

    def __eq__(self, other):
        if type(other) == LazySequence:
            self.realise_all()
            other.realise_all()
            return self.__realised_segment == other._LazySequence__realised_segment

        # A LazySequence can be equal to a list, a la Clojure
        elif type(other) == list:
            self.realise_all()
            return other == list(self.__realised_segment)

        # A LazySequence can be equal to a tuple, a la Clojure
        elif type(other) == tuple:
            self.realise_all()
            return other == self.__realised_segment

        else:
            return False

    def __hash__(self):
        """
        We want the hash of a lazysequence to not depend on how realised it is.
        i.e. it should be a hash of the seq of realised values
        """
        self.realise_all()
        return hash(self.__realised_segment)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getstate__(self):
        self.realise_all()
        return self.__realised_segment

    def __setstate__(self, state):
        self.__realised_segment = state
        self.__realised_segment_size = len(state)
        self.realised = True
        self.print_length = 100

    def realise_to(self, n):
        """
        Realises the lazy sequence up to the nth element.
        """
        if not self.realised:
            while not (self.realised or self.__realised_segment_size >= n):
                self.realise_next()

    def realise_next(self):
        """
        Realises the next unrealised element
        """
        try:
            self.__realised_segment = self.__realised_segment + (self.__source_it.next(),)
            self.__realised_segment_size += 1
        except StopIteration:
            self.realised = True

    def realise_all(self):
        """
        Realises the entire sequence.
        """
        if not self.realised:
            for x in self.__source_it:
                self.__realised_segment = self.__realised_segment + (x,)
                self.__realised_segment_size += 1
            self.realised = True
