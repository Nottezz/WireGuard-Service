import ipaddress
import logging

from wireguard_service.infrastructure.wireguard._clients import WGClient
from wireguard_service.schemas.interface import Interface

logger = logging.getLogger(__name__)


def get_config(client: WGClient, interface: str = "wg0") -> Interface:
    return client.show(interface=interface)


def get_next_allowed_ip(
    client: WGClient, interface: str, subnet: str = "10.20.30.0/24"
) -> str:
    config = get_config(client, interface=interface)

    used_ips = set()
    for peer in config.peers:
        for ip in peer.allowed_ips:
            network = ipaddress.ip_network(ip, strict=False)
            used_ips.add(network.network_address)

    network = ipaddress.ip_network(subnet, strict=False)
    hosts = list(network.hosts())

    for host in hosts[1:]:  # пропускаем .1
        if host not in used_ips:
            return f"{host}/32"

    raise RuntimeError("No available IPs in subnet")


def add_peer(
    client: WGClient,
    interface: str,
    allowed_ips: list[str] | None = None,
    endpoint: str | None = None,
    persistent_keepalive: int | None = None,
) -> dict:
    logger.debug("Allowed IPs: %s", allowed_ips)
    if allowed_ips is None:
        next_ip = get_next_allowed_ip(client, interface=interface)
        logger.debug("Next IP: %s", next_ip)
        allowed_ips = [next_ip]

    return client.add_peer_with_keys(
        interface=interface,
        allowed_ips=allowed_ips,
        endpoint=endpoint,
        persistent_keepalive=persistent_keepalive,
    )


def remove_peer(client: WGClient, interface: str, public_key: str) -> dict:
    return client.remove_peer_from_interface(interface=interface, public_key=public_key)
