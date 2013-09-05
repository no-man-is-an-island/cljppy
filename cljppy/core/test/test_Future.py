import time
import pytest
from cljppy import doseq
from cljppy.core.Future import Future


def test_futures_are_awesome():
    start_time = time.time()
    f = Future(time.sleep, 0.1)
    g = Future(time.sleep, 0.1)
    h = Future(time.sleep, 0.1)

    doseq(Future.deref, [f, g, h])

    assert time.time() - start_time < 0.2


def test_future_can_handle_exceptions():
    my_exception = Exception("This is a foo")

    def _foo():
        raise my_exception

    f = Future(_foo)

    with pytest.raises(Exception) as e:
        f()
        assert e.message == "This is a foo"

    assert isinstance(f(), Exception)