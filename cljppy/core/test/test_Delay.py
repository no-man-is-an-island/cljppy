import pytest
from cljppy.core.Delay import Delay


def test_delay_delays_things():

    x = ['before foo']
    def _foo():
        x[0] = 'after foo'
        return x[0]

    d = Delay(_foo)

    assert x == ['before foo']
    assert d() == 'after foo'
    assert x == ['after foo']


def test_delay_can_handle_exceptions():
    my_exception = Exception()

    def _foo():
        raise my_exception

    f = Delay(_foo)

    with pytest.raises(Exception) as e:
        f()
        assert e == my_exception

    with pytest.raises(Exception) as e:
        f()
        assert e == my_exception