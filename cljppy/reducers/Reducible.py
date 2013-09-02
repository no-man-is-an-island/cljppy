from cljppy.core import identity


class Reducible(object):
    def __init__(self, collection, reducer=identity):
        if isinstance(collection, Reducible):
            self.__collection = collection
            self.__reducer = lambda x: collection.reducer(reducer(x))

        else:
            self.__collection = collection
            self.__reducer = reducer

    def __iter__(self):
        return iter(self.__collection)

    def reducer(self):
        return self.reducer