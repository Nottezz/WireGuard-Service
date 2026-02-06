from wireguard_service.schemas.servers import ServerRead
from wireguard_service.schemas.interface import Interface
from wireguard_service.schemas.peer import Peer
from wireguard_service.jinja2_templates import templates


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

def camel_case_to_snake_case(input_str: str) -> str:
    """
    >>> camel_case_to_snake_case("SomeSDK")
    'some_sdk'
    >>> camel_case_to_snake_case("RServoDrive")
    'r_servo_drive'
    >>> camel_case_to_snake_case("SDKDemo")
    'sdk_demo'

    Taken from
    https://github.com/mahenzon/ri-sdk-python-wrapper/blob/master/ri_sdk_codegen/utils/case_converter.py
    """
    chars = []
    for c_idx, char in enumerate(input_str):
        if c_idx and char.isupper():
            nxt_idx = c_idx + 1
            # idea of the flag is to separate abbreviations
            # as new words, show them in lower case
            flag = nxt_idx >= len(input_str) or input_str[nxt_idx].isupper()
            prev_char = input_str[c_idx - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                chars.append("_")
        chars.append(char.lower())
    return "".join(chars)

def render_client_config(server: ServerRead, client_private_key: str, client_address: str,) -> str:
    template = templates.get_template("client_template.config")
    context = {
        "client_private_key": client_private_key,
        "client_address": client_address,
        "server_public_key": server.public_key,
        "server_address": f"{server.host}:{server.port}",
    }
    client_config = template.render(context)
    return client_config
