from processing import *
from cljppy.core import partial


class Future(object):
    def __init__(self, f, *args):
        self.realised = False

        def f_star(q):
            q.put(f(*args))

        self.__queue = Queue()
        self.__process = Process(target=f_star, args=[q])
        self.__process.start()

    