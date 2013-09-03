import atexit
from processing import *


class Future(object):
    """
    Calls a function with the given arguments in a new
    process. Returns a future object that can be blocked on
    with .deref or () to get the result. After the first
    dereferencing, dereferencing will return the function's
    result immediately.

    Futures are automatically cancelled when the main process
    exits, so they should be 'fire and forget'. They are also
    cancelled when they are garbage collected (so beware if you're
    using them for side-effect-y things!)
    """
    def __init__(self, f, *args):
        # Only one of cancelled and realised should ever be
        # True. Really wish i could make these read only.
        self.realised = False
        self.cancelled = False

        def f_star(q):
            q.put(f(*args))
            #q.close()  # TODO: Check that this does something

        self.__queue = Queue()
        self.__process = Process(target=f_star, args=[self.__queue])
        self.__process.start()
        atexit.register(self.cancel)

    def __call__(self):
        return self.deref()

    def __del__(self):
        self.finalise()

    def deref(self):
        if self.cancelled:
            return None

        if not self.realised:
            self.value = self.__queue.get()
            self.finalise()
            self.realised = True

        return self.value

    def cancel(self):
        if not self.realised:
            self.finalise()
            self.cancelled = True

    def finalise(self):
        self.__queue.close()
        self.__queue.jointhread()
        self.__process.join()
        self.__process.terminate()