# -*- encoding: utf-8 -*-

"""Handle event notification services endpoints."""

from abc import abstractmethod
from typing import Any

from ..apirequest import APIRequest


class ENS(APIRequest):
    """ENS - class to handle the event notification services endpoints."""

    ENDPOINT = ""
    METHOD = "GET"
    EXPECTED_STATUS = 0

    @abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        """Instantiate an ENS APIRequest instance.

        Parameters
        ----------
        kwargs: kwargs (optional)
            optional keyword arguments to be provided by the derived
            request class

        """
        endpoint = self.ENDPOINT.format(**kwargs)
        super(ENS, self).__init__(
            endpoint, expected_status=self.EXPECTED_STATUS, method=self.METHOD
        )
