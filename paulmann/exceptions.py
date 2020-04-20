"""Exceptions for Paulmann Lights."""

class PaulmannError(Exception):
    """Generic Paulmann Light exception."""
    pass


class PaulmannConnectionError(PaulmannError):
    """ Paulmann connection exception."""
    pass

class PaulmannAuthenticationError(PaulmannError):
    """ Paulmann connection exception."""
    pass
