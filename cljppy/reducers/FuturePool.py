from cljppy.sequence import partition
from cljppy.reducers.FutureConsumer import FutureConsumer
from threading import Thread


class FuturePool(object):
    def __init__(self, f, data, poolsize=4, chunksize=512):
        self.__poolsize = poolsize
        self.__pool = []
        self.__partitions = partition(chunksize, data)
        self.__position = 0

        for _ in range(poolsize):
            consumer = FutureConsumer(f, self.__partitions[self.__position])
