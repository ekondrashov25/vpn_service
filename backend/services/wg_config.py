from backend.db.models import Peer


DEFAULT_DNS = "1.1.1.1"
PERSISTENT_KEEPALIVE = 25
DEFAULT_ALLOWED_IPS = "0.0.0.0/0"


def generate_wg_config(peer: Peer) -> str:

    server = peer.server

    if server is None:
        raise ValueError("Peer has no associated VPN server")

    config = f"""
    [Interface]
    PrivateKey = {peer.private_key}
    Address = {peer.ip_address}/32
    DNS = {DEFAULT_DNS}

    [Peer]
    PublicKey = {server.public_key}
    Endpoint = {server.endpoint}
    AllowedIPs = {DEFAULT_ALLOWED_IPS}
    PersistentKeepalive = {PERSISTENT_KEEPALIVE}
    """.strip()

    return config
