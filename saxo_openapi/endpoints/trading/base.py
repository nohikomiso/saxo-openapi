"""Handle trading endpoints."""

from abc import abstractmethod
from typing import Any

from ..apirequest import APIRequest


class Trading(APIRequest):
    """Trading - class to handle the trading endpoints."""

    ENDPOINT = ""
    METHOD = "GET"
    EXPECTED_STATUS = 0

    @abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        """Instantiate a Trading APIRequest instance.

        Parameters
        ----------
        kwargs: kwargs (optional)
            optional keyword arguments to be provided by the derived
            request class

        """
        endpoint = self.ENDPOINT.format(**kwargs)
        super(Trading, self).__init__(endpoint, expected_status=self.EXPECTED_STATUS, method=self.METHOD)
