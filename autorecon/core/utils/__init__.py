import socket

def resolve_ip(host):
    try:
        ip = socket.gethostbyname(host)
        print(f"[+] Resolved {host} to {ip}")
        return ip
    except socket.gaierror:
        print(f"[-] Could not resolve hostname: {host}")
        return host

def parse_ports(port_str):
    ports = set()
    for part in port_str.split(','):
        if '-' in part:
            start, end = part.split('-')
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(ports)

def get_top_ports(n):
    # Top ports based on frequency — can be expanded
    top_ports = [
        21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993,
        995, 1723, 3306, 3389, 5900, 8080
    ]
    return top_ports[:n]
