"""Proxy configuration for Session()
"""
import ipaddress

from jobfunnel.config import BaseConfig


class ProxyConfig(BaseConfig):
    """Simple config object to contain proxy configuration
    """

    def __init__(self, protocol: str, ip_address: str, port: int) -> None:
        super().__init__()
        self.protocol = protocol
        self.ip_address = ip_address
        self.port = port

    @property
    def url(self) -> str:
        """Get the url string for use in a Session.proxies object
        """
        return f"{self.protocol}://{self.ip_address}:{self.port}"

    def validate(self) -> None:
        """Validate the format of ip addr and port
        """
        try:
            # try to create an IPv4 address
            ipaddress.IPv4Address(self.ip_address)
        except:
            raise ValueError(f"{self.ip_address} is not a valid IPv4 address")

        if not isinstance(self.port, int):
            raise ValueError("Port must be an integer")

        if not self.protocol:
            raise ValueError("Protocol is not set")
