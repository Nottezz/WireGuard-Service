from wireguard_service.infrastructure.wireguard._clients import WGClient
from wireguard_service.schemas.interface import Interface


def get_config(client: WGClient, interface: str = "wg0") -> Interface:
    return client.show(interface=interface)


def add_peer(
    client: WGClient,
    interface: str,
    allowed_ips: list[str],
    endpoint: str | None = None,
    persistent_keepalive: int | None = None,
) -> dict:
    return client.add_peer_with_keys(
        interface=interface,
        allowed_ips=allowed_ips,
        endpoint=endpoint,
        persistent_keepalive=persistent_keepalive,
    )


def remove_peer(client: WGClient, interface: str, public_key: str) -> dict:
    return client.remove_peer_from_interface(interface=interface, public_key=public_key)
