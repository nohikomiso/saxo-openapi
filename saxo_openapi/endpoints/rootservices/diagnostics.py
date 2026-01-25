"""Handle root-services diagnostics endpoints.

See: docs/api/rootservices/diagnostics.md
"""

from ..decorators import endpoint
from .base import RootService


@endpoint("openapi/root/v1/diagnostics/get/")
class Get(RootService):
    """Send a GET request and get a 200 OK response back."""

    RESPONSE_DATA = None

    def __init__(self) -> None:
        super(Get, self).__init__()


@endpoint("openapi/root/v1/diagnostics/post/", "POST")
class Post(RootService):
    """Send a POST request and get a 200 OK response back."""

    RESPONSE_DATA = None

    def __init__(self) -> None:
        super(Post, self).__init__()


@endpoint("openapi/root/v1/diagnostics/put/", "PUT")
class Put(RootService):
    """Send a PUT request and get a 200 OK response back."""

    RESPONSE_DATA = None

    def __init__(self) -> None:
        super(Put, self).__init__()


@endpoint("openapi/root/v1/diagnostics/delete/", "DELETE")
class Delete(RootService):
    """Send a DELETE request and get a 200 OK response back."""

    RESPONSE_DATA = None

    def __init__(self) -> None:
        super(Delete, self).__init__()


@endpoint("openapi/root/v1/diagnostics/patch/", "PATCH")
class Patch(RootService):
    """Send a PATCH request and get a 200 OK response back."""

    RESPONSE_DATA = None

    def __init__(self) -> None:
        super(Patch, self).__init__()


@endpoint("openapi/root/v1/diagnostics/head/", "HEAD")
class Head(RootService):
    """Send a HEAD request and get a 200 OK response back."""

    RESPONSE_DATA = None

    def __init__(self) -> None:
        super(Head, self).__init__()


@endpoint("openapi/root/v1/diagnostics/options/", "OPTIONS")
class Options(RootService):
    """Send a OPTIONS request and get a 200 OK response back."""

    RESPONSE_DATA = None

    def __init__(self) -> None:
        super(Options, self).__init__()


@endpoint("openapi/root/v1/diagnostics/echo/")
class Echo(RootService):
    """Send any request and get a 200 OK response with verb, url,
    headers and body in the response body.
    """

    RESPONSE_DATA = None

    def __init__(self) -> None:
        super(Echo, self).__init__()
