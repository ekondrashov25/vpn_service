import ipaddress

def allocate_ip(subnet: str, used_ips: set[str], reserved_ips: set[str] | None = None) -> str: # allocate an IP address from the given subnet
    network = ipaddress.ip_network(subnet)
    reserved = reserved_ips or set()
    
    for ip in network.hosts():
        ip_str = str(ip)
        
        if ip_str in reserved:
            continue

        if ip_str not in used_ips:
            return ip_str

    raise RuntimeError("No free IPs in subnet")
