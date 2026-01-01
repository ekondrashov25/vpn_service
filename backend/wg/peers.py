from backend.wg.interface import run, WG_INTERFACE


def add_peer(public_key: str, allowed_ips: str) -> None:
    run (["wg", "set", WG_INTERFACE, "peer", public_key, "allowed-ips", f"{allowed_ips}/32"])
    
def remove_peer(public_key: str) -> None:
    run(["wg", "set", WG_INTERFACE, "peer", public_key, "remove"])