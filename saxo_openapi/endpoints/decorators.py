# -*- encoding: UTF-8 -*-

"""decorators."""

from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


def endpoint(url: str, method: str = "GET", expected_status: int = 200) -> Callable[[T], T]:
    """endpoint - decorator to manipulate the REST-service endpoint.

    The endpoint decorator sets the endpoint and the method for the class
    to access the REST-service.
    """

    def dec(obj: T) -> T:
        obj.ENDPOINT = url
        obj.METHOD = method
        obj.EXPECTED_STATUS = expected_status
        return obj

    return dec


def abstractclass(cls: Any) -> Any:
    """abstractclass - class decorator.

    make sure the class is abstract and cannot be used on it's own.

    @abstractclass
    class A(object):
        def __init__(self, *args, **kwargs):
            # logic
            pass

    class B(A):
        pass

    a = A()   # results in an AssertionError
    b = B()   # works fine
    """
    cls._ISNEVER = cls.__bases__[0].__name__
    origInit = cls.__dict__["__init__"]

    def wrapInit(self: Any, *args: Any, **kwargs: Any) -> None:
        # when the class is instantiated we can check for bases
        # we don't want it to be the base class
        if self.__class__.__bases__[-1].__name__ != self._ISNEVER:
            origInit(self, *args, **kwargs)
        else:
            raise TypeError("Use of abstract base class")

    # replace the original __init__
    wrapInit.__doc__ = origInit.__doc__
    origInit.__doc__ = ""
    cls.__init__ = wrapInit

    return cls


class extendargs:
    """'extendargs' decorator.

    Add extra arguments to the argumentlist of the constructor of the class.
    """

    def __init__(self, *loa: str) -> None:
        self.loa = loa

    def __call__(self, cls: Any) -> Any:
        # save parent class __init__
        origInit = cls.__bases__[0].__dict__["__init__"]

        def wrapInit(wself: Any, *args: Any, **kwargs: Any) -> None:
            for extraArg in self.loa:
                if extraArg in kwargs:
                    setattr(wself, extraArg, kwargs[extraArg])
                    del kwargs[extraArg]
            origInit(wself, *args, **kwargs)

        cls.__init__ = wrapInit

        return cls
