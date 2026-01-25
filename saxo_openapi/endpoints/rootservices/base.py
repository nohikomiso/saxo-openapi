"""Handle root-services diagnostics endpoints."""

from abc import abstractmethod

from ..apirequest import APIRequest


class RootService(APIRequest):
    """RootService - baseclass to handle the rootservice endpoints."""

    ENDPOINT = ""
    METHOD = "GET"
    EXPECTED_STATUS = 0

    @abstractmethod
    def __init__(self, ContextId: str | None = None, ReferenceId: str | None = None) -> None:
        """Instantiate a RootService APIRequest instance."""
        endpoint = self.ENDPOINT.format(ContextId=ContextId, ReferenceId=ReferenceId)
        super(RootService, self).__init__(endpoint, method=self.METHOD, expected_status=self.EXPECTED_STATUS)
