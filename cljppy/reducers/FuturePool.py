from cljppy import doseq, partition_all, partial, concat
from cljppy.reducers.FutureConsumer import FutureConsumer
from threading import Thread
from multiprocessing import cpu_count


class FuturePool(object):
    def __init__(self, f, data, poolsize=cpu_count(), chunksize=512):
        self.__poolsize = poolsize
        self.__pool = []
        self.values = []
        self.__partitions = partition_all(chunksize, data)
        self.__position = 0
        self.realised = False
        self.all_work_delivered = False
        self.__partitions.realise_to(self.__poolsize)

        for _ in range(poolsize):
            self.__pool.append(FutureConsumer(partial(map, f)))

        self.dispatch()
        self.__blocking_thread = Thread(target=self.__block)
        self.__blocking_thread.start()

    def dispatch(self):

        if not self.all_work_delivered:
            for consumer in self.__pool:
                if not self.all_work_delivered:
                    try:
                        part = self.__partitions[self.__position]
                        consumer.put(part)
                    except IndexError:
                        consumer.cancel()
                        self.all_work_delivered = True
                    self.__position += 1
                else:
                    consumer.cancel()

            self.__partitions.realise_to(self.__position + self.__poolsize)

    def deref(self):
        if not self.realised:
            self.__blocking_thread.join()
        return concat(*self.values)

    def __block(self):
        flag = True
        while flag:
            for consumer in self.__pool:
                if not consumer.cancelled:
                    self.values.append(consumer.get())
            flag = not self.all_work_delivered
            self.dispatch()


        doseq(FutureConsumer.cancel, self.__pool)
        self.realised = True
        return
