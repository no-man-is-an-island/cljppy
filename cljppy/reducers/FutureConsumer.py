import atexit
from processing import *


class FutureConsumer(object):
    def __init__(self, f, vals):
        # Only one of cancelled and realised should ever be
        # True. Really wish i could make these read only.
        self.realised = False
        self.cancelled = False

        def f_star(work_q, result_q):
            v = work_q.get()

            while not v == "POISON_PILL_CLJPPY":
                result_q.put(f(v))
                v = work_q.get()
            result_q.put("POISON_PILL_CLJPPY")

        self.__work_queue = Queue()
        self.__result_queue = Queue()
        self.__process = Process(target=f_star, args=[self.__work_queue, self.__result_queue])
        self.__process.start()
        self.values = []
        atexit.register(self.cancel)

        for val in vals:
            self.__work_queue.put(val)
        self.__work_queue.put("POISON_PILL_CLJPPY")

    def __call__(self):
        return self.deref()

    def __del__(self):
        self.finalise()

    def deref(self):
        if self.cancelled:
            return None

        if not self.realised:
            value = self.__result_queue.get()

            while not value == "POISON_PILL_CLJPPY":
                self.values.append(value)

                value = self.__result_queue.get()
            self.finalise()
            self.realised = True

        return self.values

    def cancel(self):
        if not self.realised:
            self.finalise()
            self.cancelled = True

    def finalise(self):
        self.__work_queue.close()
        self.__work_queue.jointhread()
        self.__result_queue.close()
        self.__result_queue.jointhread()
        self.__process.join()
        self.__process.terminate()