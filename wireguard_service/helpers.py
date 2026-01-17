from wireguard_service.schemas.interface import Interface
from schemas.peer import Peer


def parse_wg_show(output: str) -> Interface:
    lines = output.splitlines()
    iface_data = {}
    peers = []
    current_peer = None

    for line in lines:
        line = line.strip()
        if not line:
            if current_peer:
                peers.append(current_peer)
                current_peer = None
            continue

        if line.startswith("interface:"):
            iface_data["name"] = line.split(":", 1)[1].strip()
        elif line.startswith("public key:") and current_peer is None:
            iface_data["public_key"] = line.split(":", 1)[1].strip()
        elif line.startswith("private key:"):
            iface_data["private_key"] = line.split(":", 1)[1].strip()
        elif line.startswith("listening port:"):
            iface_data["listening_port"] = int(line.split(":", 1)[1].strip())
        elif line.startswith("peer:"):
            if current_peer:
                peers.append(current_peer)
            current_peer = {"public_key": line.split(":", 1)[1].strip()}
        elif current_peer is not None:
            key, val = line.split(":", 1)
            key = key.lower().replace(" ", "_")

            # Обрабатываем allowed IPs как список
            if key == "allowed_ips":
                current_peer["allowed_ips"] = [
                    ip.strip() for ip in val.strip().split(",") if ip.strip()
                ]
            else:
                current_peer[key] = val.strip()

    if current_peer:
        peers.append(current_peer)

    return Interface(peers=[Peer(**p) for p in peers], **iface_data)
