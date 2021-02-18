# FIXME
from unittest.mock import patch

import pytest

from jobfunnel.config import ProxyConfig


@pytest.mark.parametrize("protocol, ip_address, port, expected_protocol, expected_ip, expected_port", [
    ("test_str", "255.255.255.255", 5000, "test_str", "255.255.255.255", 5000),
    ("some_protocol", "111.111.111.111", 8000, "some_protocol", "111.111.111.111", 8000),
])
def test_proxy_config_init(protocol, ip_address, port, expected_protocol, expected_ip, expected_port):
    prx = ProxyConfig(protocol, ip_address, port)
    protocol_attr = prx.__getattribute__("protocol")
    ip_address_attr = prx.__getattribute__("ip_address")
    port_attr = prx.__getattribute__("port")
    assert protocol_attr == expected_protocol
    assert ip_address_attr == expected_ip
    assert port_attr == expected_port


@pytest.mark.parametrize("protocol, ip_address, port, expected_result", [
    ("test_str", "255.255.255.255", 5000, "test_str://255.255.255.255:5000"),
    ("some_protocol", "111.111.111.111", 8000, "some_protocol://111.111.111.111:8000"),
])
def test_proxy_config_url(protocol, ip_address, port, expected_result):
    prx = ProxyConfig(protocol, ip_address, port)
    result = prx.url
    assert result == expected_result


@patch('jobfunnel.config.ProxyConfig.validate')
def test_proxy_config_validate_ip_positive(mock_validate):
    prx = ProxyConfig("some_protocol", "255.255.255.255", 5000)
    prx.validate()
    assert prx.validate == mock_validate
    assert mock_validate.called


@pytest.mark.parametrize("protocol, ip_address, port", [
    ("test_str", "255", 5000),
    ("some_protocol", "not an ip address", 8000),
])
def test_proxy_config_validate_ip_negative(protocol, ip_address, port):
    prx = ProxyConfig(protocol, ip_address, port)
    with pytest.raises(ValueError):
        prx.validate()


@pytest.mark.parametrize("protocol, ip_address, port", [
    ("test_str", "255.255.255.255", 2.0),
    ("some_protocol", "255.255.255.255", "8000"),
])
def test_proxy_config_validate_port_negative(protocol, ip_address, port):
    prx = ProxyConfig(protocol, ip_address, port)
    with pytest.raises(ValueError):
        prx.validate()


@pytest.mark.parametrize("protocol, ip_address, port", [
    ("", "255.255.255.255", True),
    ("", "255.255.255.255", "8000"),
])
def test_proxy_config_validate_protocol_negative(protocol, ip_address, port):
    prx = ProxyConfig(protocol, ip_address, port)
    with pytest.raises(ValueError):
        prx.validate()
