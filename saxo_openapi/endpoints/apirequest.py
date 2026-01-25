# -*- coding: utf-8 -*-

"""Handling of API requests."""

from abc import ABCMeta, abstractmethod
from typing import Any, Optional


class APIRequest(metaclass=ABCMeta):
    """Base Class for API-request classes."""

    @abstractmethod
    def __init__(
        self, endpoint: str, expected_status: int, method: str = "GET"
    ) -> None:
        """Instantiate an API request.

        Parameters
        ----------
        endpoint : string
            the URL format string

        method : string
            the method for the request. Default: GET.

        expected_status : int
            the expected HTTP status code for a successful response
        """
        self._expected_status = expected_status
        self._status_code: Optional[int] = None
        self._response: Any = None

        self._endpoint = endpoint
        self.method = method

    @property
    def expected_status(self) -> int:
        return self._expected_status

    @property
    def status_code(self) -> Optional[int]:
        return self._status_code

    @status_code.setter
    def status_code(self, value: int) -> None:
        if value != self._expected_status:
            raise ValueError("{} {} {:d}".format(self, self.method, value))
        self._status_code = value

    @property
    def response(self) -> Any:
        """response - get the response of the request."""
        return self._response

    @response.setter
    def response(self, value: Any) -> None:
        """response - set the response of the request."""
        self._response = value

    def __str__(self) -> str:
        """return the endpoint."""
        return self._endpoint
