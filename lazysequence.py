from itertools import imap
from cljitertools import take


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

    def __iter__(self):
        return self


class LazySequence(object):
    def __init__(self, source, printlength = 100):
        """
        Takes a 'source', which can be a generator or an
        iterable object.
        """
        self.realised = False
        self.__realised_segment = []
        self.__source_it = iter(source)
        self.print_length = printlength
        try:
            self.__realised_segment.append(self.__source_it.next())
        except StopIteration:
            self.realised = True

    def __getitem__(self, item):
        if type(item) is slice:
            s = []
            for idx in range(item.start, item.stop):
                s.append(self[idx])
            return s

        if item >= len(self.__realised_segment):
            if self.realised:
                raise IndexError("index out of range")
            while (not self.realised) and len(self.__realised_segment) != item + 1:
                self.realise_next()
            return self[item]
        else:
            if item == len(self.__realised_segment):
                raise IndexError("index out of range")
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
        if self.realised and self.print_length >= len(self.__realised_segment):
            return str(self.__realised_segment)
        return "[" + ', '.join(take(self.print_length,
                                    imap(str, self.__realised_segment))) + ", ...]"

    def __eq__(self, other):
        if type(other) == LazySequence:
            self.realise_all()
            other.realise_all()

            return self.__realised_segment == other._LazySequence__realised_segment

        elif type(other) == list:
            self.realise_all()
            return other == self.__realised_segment

        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def realise_next(self):
        try:
            self.__realised_segment.append(self.__source_it.next())
        except StopIteration:
            self.realised = True

    def realise_all(self):
        if not self.realised:
            for x in self.__source_it:
                self.__realised_segment.append(x)
            self.realised = True
