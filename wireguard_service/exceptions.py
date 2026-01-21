class WireGuardBaseError(Exception):
    """
    Base exception for service
    """


class PeerAlreadyExistsError(WireGuardBaseError):
    """
    Raised when a peer already exists
    """
