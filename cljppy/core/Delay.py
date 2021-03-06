from cljppy.core import partial


class Delay():
    """
    Delayed computation of a function. Computation can
    be forced by calling the Delay as a function, or using .deref().
    After the first deref, the return value of the function
    will just be returned immediately.
    """
    def __init__(self, f, *args):
        self.__computation = partial(f, *args)
        self.realised = False

    def __call__(self):
        return self.deref()

    def deref(self):
        if not self.realised:
            try:
                self.__value = self.__computation()
            except Exception,e :
                self.__exception = e
                self.realised = True

            self.realised = True

        if hasattr(self, "__exception"):
            raise self.__exception

        return self.__value