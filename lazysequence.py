from itertools import imap
from cljitertools import take


class LazySequenceIterator(object):
    __lazyseq = None
    __index = 0


    def __init__(self, lazyseq):
        self.__lazyseq = lazyseq

    def next(self):
        try:
            self.__index += 1
            return self.__lazyseq[self.__index - 1]
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return iter(self.__lazyseq)


class LazySequence(object):
    __realised_segment = []
    realised = False
    print_length = 100
    __source_it = None


    def __init__(self, source, printlength = 100):
        """
        Takes a 'source', which can be a generator or an
        iterable object.
        """
        self.__source_it = iter(source)
        self.print_length = printlength
        try:
            self.__realised_segment.append(self.__source_it.next())
        except StopIteration:
            self.realised = True


    def __getitem__(self, item):
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
        return "[" + ', '.join(take(self.print_length,
                                    imap(str, self.__realised_segment))) + ", ...]"


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
