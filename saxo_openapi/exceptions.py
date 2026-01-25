"""Exceptions."""


class StreamTerminated(Exception):
    """StreamTerminated."""


class OpenAPIError(Exception):
    """Generic error class.

    In case of HTTP response codes >= 400 this class can be used
    to raise an exception representing that error.
    """

    def __init__(self, code: int, reason: str, content: str | None = None) -> None:
        """Instantiate an OpenAPIError.

        Parameters
        ----------
        code : int (required)
            the HTTP-code of the response

        reason : str (required)
            the reason of the exceptions

        content : str (optional)
            the content
        """
        self.code = code
        self.reason = reason
        self.content = content

        message = f"HTTP error: {code}, reason: {reason}"
        # if error content is returned, include in exception
        if self.content:
            message += f", errorcontent: {content}"

        super(OpenAPIError, self).__init__(message)
