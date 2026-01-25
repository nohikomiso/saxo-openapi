"""Handle charts endpoints."""

from abc import abstractmethod
from typing import Any

from ..apirequest import APIRequest


class Charts(APIRequest):
    """Charts - class to handle the charts endpoints."""

    ENDPOINT = ""
    METHOD = "GET"
    EXPECTED_STATUS = 0

    @abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        """Instantiate a Charts APIRequest instance.

        Parameters
        ----------
        kwargs: kwargs (optional)
            optional keyword arguments to be provided by the derived
            request class

        """
        endpoint = self.ENDPOINT.format(**kwargs)
        super(Charts, self).__init__(endpoint, expected_status=self.EXPECTED_STATUS, method=self.METHOD)
