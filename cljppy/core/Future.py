import atexit
from multiprocessing import *


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
            q.send(f(*args))
            q.close()

        self.__pipe = Pipe()
        self.__process = Process(target=f_star, args=[self.__pipe[0]])
        self.__process.start()
        atexit.register(self.cancel)

    def __call__(self):
        return self.deref()

    def __del__(self):
        self._finalise()

    def deref(self):
        if self.cancelled:
            return None

        if not self.realised:
            self.value = self.__pipe[1].recv()
            self._finalise()
            self.realised = True

        return self.value

    def cancel(self):
        if not self.realised:
            self._finalise()
            self.cancelled = True

    def _finalise(self):
        self.__pipe[0].close()
        self.__pipe[1].close()
        self.__process.join()
        self.__process.terminate()